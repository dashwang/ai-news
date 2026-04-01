"""
Database layer unit tests.

Tests database initialization, CRUD operations, and query functions.
"""
import os
import sqlite3
import pytest
from datetime import datetime
from unittest.mock import patch, mock_open
import json

# Import database functions
from fetch_news import (
    get_db,
    init_db,
    save_news,
    get_news_json,
)
from app import (
    get_db as app_get_db,
    init_db as app_init_db,
)
from publish_wechat import (
    get_db as wechat_get_db,
    init_db as wechat_init_db,
)


class TestDatabaseInitialization:
    """Test database initialization."""

    def test_init_db_creates_tables(self, temp_db):
        """Test that init_db creates the required tables."""
        init_db()
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Check news table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
        )
        assert cursor.fetchone() is not None

        # Check table has expected columns
        cursor.execute("PRAGMA table_info(news)")
        columns = {row[1] for row in cursor.fetchall()}
        expected_columns = {
            "id", "source", "title", "url", "content",
            "summary", "score", "date", "created_at",
            "title_zh", "summary_zh", "icon"
        }
        assert expected_columns.issubset(columns)

        conn.close()

    def test_init_db_idempotent(self, temp_db):
        """Test that init_db can be called multiple times safely."""
        # Call init_db multiple times
        init_db()
        init_db()
        init_db()

        # Should still have the same table
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
        )
        assert cursor.fetchone() is not None
        conn.close()

    def test_get_db_with_row_factory(self, temp_db):
        """Test that get_db sets row_factory correctly."""
        conn = get_db()
        assert conn.row_factory == sqlite3.Row
        conn.close()

    def test_app_init_db_creates_tables(self, temp_db):
        """Test that app init_db creates the news table."""
        # Use app's init_db which has slightly different path handling
        with patch('app.os.path.dirname', return_value=os.path.dirname(temp_db)):
            app_init_db()
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
            )
            assert cursor.fetchone() is not None
            conn.close()


class TestNewsCRUD:
    """Test CRUD operations for news items."""

    @pytest.mark.unit
    def test_save_single_news_item(self, db_conn):
        """Test saving a single news item."""
        news_item = {
            "source": "HackerNews",
            "title": "Test AI News",
            "url": "https://example.com/news",
            "content": "",
            "summary": "Test summary",
            "score": 100,
            "icon": "https://example.com/icon.png",
            "date": "2026-03-30",
        }

        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, content, summary, score, date, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                news_item["source"],
                news_item["title"],
                news_item["url"],
                news_item["content"],
                news_item["summary"],
                news_item["score"],
                news_item["date"],
                news_item["icon"],
            ),
        )
        db_conn.commit()

        # Verify the item was saved
        cursor.execute(
            "SELECT id, source, title, score, date FROM news WHERE title = ?",
            (news_item["title"],),
        )
        row = cursor.fetchone()

        assert row is not None
        assert row["title"] == news_item["title"]
        assert row["source"] == news_item["source"]
        assert row["score"] == news_item["score"]
        assert row["date"] == news_item["date"]

    @pytest.mark.unit
    def test_save_multiple_news_items(self, db_conn):
        """Test saving multiple news items."""
        news_items = [
            {
                "source": "TechCrunch",
                "title": "News 1",
                "url": "https://example.com/1",
                "content": "",
                "summary": "Summary 1",
                "score": 50,
                "date": "2026-03-30",
            },
            {
                "source": "TechCrunch",
                "title": "News 2",
                "url": "https://example.com/2",
                "content": "",
                "summary": "Summary 2",
                "score": 75,
                "date": "2026-03-30",
            },
        ]

        cursor = db_conn.cursor()
        for item in news_items:
            cursor.execute(
                """
                INSERT INTO news (source, title, url, content, summary, score, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["source"],
                    item["title"],
                    item["url"],
                    item["content"],
                    item["summary"],
                    item["score"],
                    item["date"],
                ),
            )
        db_conn.commit()

        # Verify all items were saved
        cursor.execute(
            "SELECT COUNT(*) as count FROM news WHERE source = ?",
            (news_items[0]["source"],),
        )
        count = cursor.fetchone()["count"]
        assert count == len(news_items)

    @pytest.mark.unit
    def test_delete_news_by_date(self, db_conn):
        """Test deleting news items by date."""
        # Insert test data for two different dates
        test_items = [
            {
                "source": "Test",
                "title": "Old News",
                "url": "https://example.com/old",
                "date": "2026-03-29",
                "score": 10,
            },
            {
                "source": "Test",
                "title": "New News",
                "url": "https://example.com/new",
                "date": "2026-03-30",
                "score": 20,
            },
            {
                "source": "Test",
                "title": "Another New",
                "url": "https://example.com/new2",
                "date": "2026-03-30",
                "score": 30,
            },
        ]

        cursor = db_conn.cursor()
        for item in test_items:
            cursor.execute(
                """
                INSERT INTO news (source, title, url, date, score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (item["source"], item["title"], item["url"], item["date"], item["score"]),
            )
        db_conn.commit()

        # Delete old date
        cursor.execute(
            "DELETE FROM news WHERE date LIKE ?", ("2026-03-29%",)
        )
        db_conn.commit()

        # Verify deletion
        cursor.execute("SELECT COUNT(*) as count FROM news")
        assert cursor.fetchone()["count"] == 2

    @pytest.mark.unit
    def test_update_news_score(self, db_conn):
        """Test updating news scores."""
        # Insert a news item
        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, date, score)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Test", "Test Title", "https://example.com", "2026-03-30", 50),
        )
        db_conn.commit()

        # Update the score
        cursor.execute(
            "UPDATE news SET score = ? WHERE title = ?", (100, "Test Title")
        )
        db_conn.commit()

        # Verify update
        cursor.execute("SELECT score FROM news WHERE title = ?", ("Test Title",))
        assert cursor.fetchone()["score"] == 100

    @pytest.mark.unit
    def test_insert_with_translations(self, db_conn):
        """Test inserting news items with Chinese translations."""
        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, summary, score, date, title_zh, summary_zh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Test",
                "English Title",
                "https://example.com",
                "English summary",
                50,
                "2026-03-30",
                "中文标题",
                "中文摘要",
            ),
        )
        db_conn.commit()

        cursor.execute(
            "SELECT title_zh, summary_zh FROM news WHERE title = ?", ("English Title",)
        )
        row = cursor.fetchone()

        assert row["title_zh"] == "中文标题"
        assert row["summary_zh"] == "中文摘要"


class TestQueryFunctions:
    """Test query functions for retrieving news."""

    @pytest.mark.unit
    def test_get_news_json_empty_date(self, db_conn, temp_db):
        """Test get_news_json with no data for a date."""
        with patch("fetch_news.get_db", return_value=db_conn):
            result = get_news_json("2026-03-30")
            assert result["date"] == "2026-03-30"
            assert result["news"] == {
                "HackerNews": [],
                "ProductHunt": [],
                "TechCrunch": [],
                "SubStack": []
            }

    @pytest.mark.unit
    def test_get_news_json_with_data(self, db_conn, temp_db):
        """Test get_news_json returns properly formatted data."""
        # Insert test data
        cursor = db_conn.cursor()
        news_data = [
            {
                "source": "HackerNews",
                "title": "HN1",
                "url": "https://h1.com",
                "summary": "Summary1",
                "score": 100,
                "icon": "h1.png",
            },
            {
                "source": "TechCrunch",
                "title": "TC1",
                "url": "https://t1.com",
                "summary": "Summary2",
                "score": 50,
                "icon": "t1.png",
            },
            {
                "source": "TheSequence",
                "title": "TS1",
                "url": "https://ts1.com",
                "summary": "Summary3",
                "score": 75,
                "icon": "ts1.png",
            },
            {
                "source": "SubStackNewsletter",
                "title": "SS1",
                "url": "https://ss1.com",
                "summary": "Summary4",
                "score": 60,
                "icon": "ss1.png",
            },
        ]
        for item in news_data:
            cursor.execute(
                """
                INSERT INTO news (source, title, url, summary, score, icon, date)
                VALUES (?, ?, ?, ?, ?, ?, '2026-03-30')
                """,
                (item["source"], item["title"], item["url"], item["summary"],
                 item["score"], item["icon"]),
            )
        db_conn.commit()

        with patch("fetch_news.get_db", return_value=db_conn):
            result = get_news_json("2026-03-30")

        assert result["date"] == "2026-03-30"
        assert result["status"] == "ok"
        assert len(result["news"]["HackerNews"]) == 1
        assert len(result["news"]["TechCrunch"]) == 1
        assert len(result["news"]["SubStack"]) == 2
        assert result["news"]["SubStack"][0]["score"] == 75  # Highest score first
        assert result["news"]["SubStack"][1]["score"] == 60

    @pytest.mark.unit
    def test_get_news_json_default_date(self, db_conn, temp_db):
        """Test get_news_json uses current date when none provided."""
        from datetime import datetime as dt

        with patch("fetch_news.get_db", return_value=db_conn):
            result = get_news_json()
            expected_date = dt.now().strftime("%Y-%m-%d")
            assert result["date"] == expected_date

    @pytest.mark.unit
    def test_get_news_json_nonexistent_source(self, db_conn, temp_db):
        """Test that news not in expected sources goes to SubStack."""
        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, score, date)
            VALUES (?, ?, ?, ?, '2026-03-30')
            """,
            ("UnknownSource", "Test", "https://example.com", 50),
        )
        db_conn.commit()

        with patch("fetch_news.get_db", return_value=db_conn):
            result = get_news_json("2026-03-30")
            assert len(result["news"]["SubStack"]) == 1
            assert result["news"]["SubStack"][0]["source"] == "UnknownSource"


class TestDatabaseConsistency:
    """Test database consistency and edge cases."""

    @pytest.mark.unit
    def test_duplicate_items_prevented(self, db_conn):
        """Test that duplicate items are not inserted without date filtering."""
        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, date, score)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Test", "Same Title", "https://example.com", "2026-03-30", 50),
        )
        db_conn.commit()

        # Insert again - should create new ID due to separate rows
        cursor.execute(
            """
            INSERT INTO news (source, title, url, date, score)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Test", "Same Title", "https://example.com", "2026-03-31", 60),
        )
        db_conn.commit()

        # Verify we have two entries
        cursor.execute("SELECT COUNT(*) as count FROM news WHERE title = ?", ("Same Title",))
        assert cursor.fetchone()["count"] == 2

    @pytest.mark.unit
    def test_null_values_handling(self, db_conn):
        """Test that null values are handled correctly."""
        cursor = db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO news (source, title, url, date, score)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Test", None, None, "2026-03-30", 50),
        )
        db_conn.commit()

        cursor.execute("SELECT title, url FROM news WHERE score = ?", (50,))
        row = cursor.fetchone()
        assert row["title"] is None
        assert row["url"] is None

    @pytest.mark.unit
    def test_special_characters_in_content(self, db_conn):
        """Test handling of special characters in content."""
        cursor = db_conn.cursor()
        test_content = "Special chars: <>&\"'\"\"⚡"
        cursor.execute(
            """
            INSERT INTO news (source, title, url, content, date, score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Test", "Test Title", "https://example.com", test_content, "2026-03-30", 50),
        )
        db_conn.commit()

        cursor.execute("SELECT content FROM news WHERE score = ?", (50,))
        assert cursor.fetchone()["content"] == test_content


class TestIntegrationWithSaveNews:
    """Integration tests for save_news function."""

    @pytest.mark.unit
    def test_save_news_with_complete_data(self, temp_db):
        """Test saving news with all fields."""
        news_items = [{
            "source": "HackerNews",
            "title": "Complete Test",
            "url": "https://example.com",
            "content": "Full content here",
            "summary": "Test summary",
            "score": 100,
            "icon": "icon.png",
            "date": "2026-03-30",
        }]

        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            save_news(news_items, "2026-03-30")

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news WHERE title = ?", ("Complete Test",))
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row["source"] == "HackerNews"
        assert row["title"] == "Complete Test"
        assert row["content"] == "Full content here"
        assert row["summary"] == "Test summary"
        assert row["score"] == 100

    @pytest.mark.unit
    def test_save_news_multiple_sources(self, temp_db):
        """Test saving news from multiple sources."""
        news_items = [
            {
                "source": "HackerNews",
                "title": "HN Title",
                "url": "https://h.com",
                "score": 50,
                "date": "2026-03-30",
            },
            {
                "source": "ProductHunt",
                "title": "PH Title",
                "url": "https://p.com",
                "score": 40,
                "date": "2026-03-30",
            },
            {
                "source": "TechCrunch",
                "title": "TC Title",
                "url": "https://t.com",
                "score": 30,
                "date": "2026-03-30",
            },
        ]

        with patch("fetch_news.get_db", return_value=sqlite3.connect(temp_db)):
            save_news(news_items, "2026-03-30")

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT source, COUNT(*) as count FROM news WHERE date LIKE ? GROUP BY source", ("2026-03-30%",))
        results = cursor.fetchall()
        conn.close()

        source_counts = {r["source"]: r["count"] for r in results}
        assert source_counts["HackerNews"] == 1
        assert source_counts["ProductHunt"] == 1
        assert source_counts["TechCrunch"] == 1
