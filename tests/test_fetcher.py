"""
RSS feed and Twitter scraper tests.

Tests news fetching, parsing, and aggregation logic.
"""
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

import pytest
import feedparser

# Import fetcher functions
from fetch_news import (
    SOURCES,
    fetch_rss_source,
    fetch_hackernews,
    fetch_all_news,
    save_news,
    get_news_json,
    init_db,
    fetch_main,
)


@pytest.fixture
def mock_feedparser_data():
    """Mock feedparser feed data."""
    return {
        "feed": {"title": "Test Feed", "link": "https://test.com"},
        "entries": [
            {
                "title": "Test Article 1",
                "link": "https://test.com/article1",
                "summary": "Test summary 1",
                "description": "Test description 1",
                "tags": [{"term": "5"}],
                "likes": "10",
            },
            {
                "title": "Test Article 2",
                "link": "https://test.com/article2",
                "summary": "Test summary 2",
                "description": "Test description 2",
                "tags": [{"term": "3"}],
                "likes": "5",
            },
            {
                "title": "Article Without Tags",
                "link": "https://test.com/no_tags",
                "summary": "No tags here",
                "description": "No tags",
            },
            {
                "title": "Article With Likes",
                "link": "https://test.com/likes",
                "summary": "Has likes",
                "likes": "20",
            },
        ],
    }


@pytest.fixture
def sample_rss_source_config():
    """Sample RSS source configuration."""
    return {
        "url": "https://techcrunch.com/feed/",
        "top_n": 5,
        "icon": "https://techcrunch.com/favicon.ico",
    }


class TestRSSSourceFetching:
    """Test RSS feed fetching."""

    @pytest.mark.unit
    def test_fetch_rss_source_success(self, mock_feedparser_data, sample_rss_source_config):
        """Test successful RSS feed fetching."""
        with patch('feedparser.parse', return_value=mock_feedparser_data):
            items = fetch_rss_source("TechCrunch", sample_rss_source_config)

        assert len(items) == 4  # All 4 entries returned
        assert items[0]["source"] == "TechCrunch"
        assert items[0]["title"] == "Test Article 1"
        assert items[0]["url"] == "https://test.com/article1"
        assert items[0]["score"] == 5  # From tags
        assert items[0]["summary"] == "Test summary 1"

    @pytest.mark.unit
    def test_fetch_rss_source_limits_to_top_n(self, mock_feedparser_data, sample_rss_source_config):
        """Test that only top_n entries are returned."""
        with patch('feedparser.parse', return_value=mock_feedparser_data):
            items = fetch_rss_source("Test", {"url": "http://test.com", "top_n": 2})

        assert len(items) == 2

    @pytest.mark.unit
    def test_fetch_rss_source_missing_attributes(self, mock_feedparser_data, sample_rss_source_config):
        """Test handling of entries with missing attributes."""
        # Modify mock to have an entry without link
        mock_feedparser_data["entries"][0]["link"] = ""
        mock_feedparser_data["entries"][0]["title"] = ""

        with patch('feedparser.parse', return_value=mock_feedparser_data):
            items = fetch_rss_source("Test", sample_rss_source_config)

        assert len(items) == 4  # Should still process all entries

    @pytest.mark.unit
    def test_fetch_rss_source_exception_handling(self, sample_rss_source_config):
        """Test exception handling during feed parsing."""
        with patch('feedparser.parse', side_effect=Exception("Network error")):
            items = fetch_rss_source("Test", sample_rss_source_config)

        assert items == []


class TestHackerNewsFetching:
    """Test HackerNews specific fetching."""

    @pytest.mark.unit
    @patch('feedparser.parse')
    def test_fetch_hackernews_default_limit(self, mock_parse):
        """Test HackerNews fetching with default top 5 limit."""
        mock_parse.return_value = {
            "entries": [
                {
                    "title": f"HN Article {i}",
                    "link": f"https://hn.com/{i}",
                    "tags": [{"term": str(5 - i)}] if i != 2 else [],
                }
                for i in range(7)  # More than 5 entries
            ],
        }

        items = fetch_hackernews()

        assert len(items) == 5  # Default limit
        assert all(item["source"] == "HackerNews" for item in items)

    @pytest.mark.unit
    @patch('feedparser.parse')
    def test_fetch_hackernews_exception_handling(self, mock_parse):
        """Test exception handling in HackerNews fetching."""
        mock_parse.side_effect = Exception("Feed error")

        items = fetch_hackernews()

        assert items == []


class TestFeedAggregation:
    """Test aggregation of feeds from multiple sources."""

    @pytest.mark.unit
    def test_fetch_all_news_with_multiple_sources(self):
        """Test fetching from multiple RSS sources."""
        with patch('feedparser.parse') as mock_parse:
            # Mock different sources to return different numbers of entries
            def mock_parse_side_effect(url):
                if "techcrunch" in url:
                    return {
                        "entries": [
                            {"title": f"TC{i}", "link": f"https://t.com/{i}"}
                            for i in range(3)
                        ],
                        "feed": {"title": "TechCrunch"},
                    }
                elif "producthunt" in url:
                    return {
                        "entries": [
                            {"title": f"PH{i}", "link": f"https://p.com/{i}"}
                            for i in range(2)
                        ],
                        "feed": {"title": "ProductHunt"},
                    }
                return {"entries": [], "feed": {"title": "Unknown"}}

            mock_parse.side_effect = mock_parse_side_effect

            items = fetch_all_news()

            assert len(items) == 5  # 3 from TechCrunch + 2 from ProductHunt
            assert len([item for item in items if item["source"] == "TechCrunch"]) == 3
            assert len([item for item in items if item["source"] == "ProductHunt"]) == 2

    @pytest.mark.unit
    def test_fetch_all_news_exception_handling(self):
        """Test exception handling when one source fails."""
        with patch('feedparser.parse') as mock_parse:
            def mock_parse_side_effect(url):
                if "techcrunch" in url:
                    return {
                        "entries": [
                            {"title": f"TC{i}", "link": f"https://t.com/{i}"}
                            for i in range(2)
                        ],
                        "feed": {"title": "TechCrunch"},
                    }
                raise Exception("Feed error")

            mock_parse.side_effect = mock_parse_side_effect

            items = fetch_all_news()

            assert len(items) == 2  # TechCrunch succeeded, others failed


class TestSaveNewsFunction:
    """Test save_news function."""

    @pytest.mark.unit
    def test_save_news_saves_items(self, temp_db):
        """Test that save_news correctly saves news items."""
        news_items = [
            {
                "source": "TechCrunch",
                "title": "News 1",
                "url": "https://example.com/1",
                "content": "Content 1",
                "summary": "Summary 1",
                "score": 50,
                "icon": "icon.png",
                "date": "2026-03-30",
            },
            {
                "source": "HackerNews",
                "title": "News 2",
                "url": "https://example.com/2",
                "content": "Content 2",
                "summary": "Summary 2",
                "score": 75,
                "icon": "",
                "date": "2026-03-30",
            },
        ]

        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            save_news(news_items, "2026-03-30")

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as count FROM news WHERE date = ?", ("2026-03-30",)
        )
        count = cursor.fetchone()["count"]
        conn.close()

        assert count == 2

    @pytest.mark.unit
    def test_save_news_deletes_existing_same_date(self, temp_db):
        """Test that save_news deletes existing items for the same date."""
        # First insert
        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            save_news(
                [{"title": "Old", "source": "Test", "url": "http://old", "score": 10, "date": "2026-03-30"}],
                "2026-03-30"
            )

        # Second insert with different items
        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            save_news(
                [{"title": "New", "source": "Test", "url": "http://new", "score": 20, "date": "2026-03-30"}],
                "2026-03-30"
            )

        # Check only new items exist
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM news WHERE date = ?", ("2026-03-30",))
        count = cursor.fetchone()["count"]
        conn.close()

        assert count == 1


class TestGetNewsJsonFunction:
    """Test get_news_json function."""

    @pytest.mark.unit
    def test_get_news_json_default_date(self, temp_db):
        """Test get_news_json returns current date when none provided."""
        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            result = get_news_json()

        assert "date" in result
        assert result["date"] == datetime.now().strftime("%Y-%m-%d")

    @pytest.mark.unit
    def test_get_news_json_with_data(self, temp_db):
        """Test get_news_json returns formatted data."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Insert test data
        cursor.execute(
            """
            INSERT INTO news (source, title, url, summary, score, icon, date)
            VALUES (?, ?, ?, ?, ?, ?, '2026-03-30')
            """,
            ("HackerNews", "HN Article", "https://hn.com", "HN Summary", 100, "h.png"),
        )
        conn.commit()
        conn.close()

        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            result = get_news_json("2026-03-30")

        assert result["date"] == "2026-03-30"
        assert result["status"] == "ok"
        assert "news" in result
        assert "HackerNews" in result["news"]
        assert len(result["news"]["HackerNews"]) == 1

    @pytest.mark.unit
    def test_get_news_json_substack_ordering(self, temp_db):
        """Test SubStack news items are sorted by score."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Insert multiple SubStack items
        for score in [50, 100, 75]:
            cursor.execute(
                """
                INSERT INTO news (source, title, url, summary, score, date)
                VALUES (?, ?, ?, ?, ?, '2026-03-30')
                """,
                ("SubStackSource", f"Score {score}", f"https://ss.com/{score}", f"Summary {score}", score),
            )
        conn.commit()
        conn.close()

        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            result = get_news_json("2026-03-30")

        # SubStack items should be sorted by score desc
        substack_items = result["news"].get("SubStack", [])
        scores = [item["score"] for item in substack_items]
        assert scores == sorted(scores, reverse=True)


class TestFetchMainFunction:
    """Test main fetch function."""

    @pytest.mark.unit
    @patch('fetch_news.init_db')
    @patch('fetch_news.fetch_all_news')
    @patch('fetch_news.save_news')
    def test_fetch_main_success(self, mock_save, mock_fetch, mock_init):
        """Test successful fetch_main execution."""
        mock_fetch.return_value = []
        mock_save.return_value = None

        # Mock datetime for consistent date
        with patch('fetch_news.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 30)

            success = fetch_main()

            assert success is True
            mock_init.assert_called_once()
            mock_fetch.assert_called_once()
            mock_save.assert_called_once()

    @pytest.mark.unit
    @patch('fetch_news.init_db')
    @patch('fetch_news.fetch_all_news', return_value=[])
    @patch('fetch_news.save_news', return_value=None)
    def test_fetch_main_with_date_argument(self, mock_save, mock_fetch, mock_init):
        """Test fetch_main with custom date."""
        with patch('fetch_news.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 30)

            success = fetch_main(date="2026-02-28")

            assert success is True
            mock_save.assert_called_once()
            # Check the date passed to save_news
            call_args = mock_save.call_args
            assert call_args[0][1] == "2026-02-28"


class TestSourcesConfiguration:
    """Test SOURCES configuration."""

    @pytest.mark.unit
    def test_sources_include_expected_feeds(self):
        """Test that expected RSS feeds are in configuration."""
        expected_feeds = [
            "TechCrunch",
            "HackerNews",
            "ProductHunt",
            "TheSequence",
            "AheadofAI",
            "LatentSpace",
        ]

        for feed in expected_feeds:
            assert feed in SOURCES, f"Expected feed {feed} not in SOURCES"

    @pytest.mark.unit
    def test_sources_have_valid_urls(self):
        """Test that all sources have valid URL patterns."""
        for source_name, config in SOURCES.items():
            url = config["url"]
            assert url.startswith("http://") or url.startswith("https://"), \
                f"{source_name} has invalid URL: {url}"

    @pytest.mark.unit
    def test_sources_top_n_is_positive(self):
        """Test that top_n is a positive integer for all sources."""
        for source_name, config in SOURCES.items():
            top_n = config["top_n"]
            assert isinstance(top_n, int), f"{source_name} top_n is not an integer"
            assert top_n > 0, f"{source_name} top_n is not positive"
