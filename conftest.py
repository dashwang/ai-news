"""Pytest configuration and shared fixtures."""
import os
import sys
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_path = temp_file.name
    temp_file.close()

    # Initialize the DB
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            content TEXT,
            summary TEXT,
            score INTEGER DEFAULT 0,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title_zh TEXT,
            summary_zh TEXT,
            icon TEXT
        )
    """)
    conn.commit()
    conn.close()

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def db_conn(temp_db):
    """Create a database connection for testing."""
    conn = sqlite3.connect(temp_db)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


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
                "likes": "5",
            },
        ],
    }


@pytest.fixture
def mock_twitter_response():
    """Mock Twitter API response."""
    return {
        "data": {
            "timeline": {
                "instructions": [
                    {
                        "type": "TimelineAddEntries",
                        "entries": [
                            {
                                "entryId": "tweet-123",
                                "content": {
                                    "tweet": {
                                        "text": "This is a test tweet about AI!",
                                        "created_at": "2026-03-30T10:00:00.000Z",
                                    }
                                },
                            }
                        ],
                    }
                ],
            }
        }
    }


@pytest.fixture
def mock_weathercone_requests():
    """Mock requests.get for weathercone API."""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "precipitation": {"value": 10, "type": "rain"},
            "temperature": 20,
            "condition": "partly-cloudy",
            "icon": "cloud-sun",
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    with patch("openai.OpenAI") as mock_client_class:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content="Translated and edited content"
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def sample_news_data():
    """Sample news data for testing."""
    return [
        {
            "source": "HackerNews",
            "title": "Test AI News",
            "url": "https://example.com/news",
            "content": "",
            "summary": "Test summary",
            "score": 100,
            "icon": "https://example.com/icon.png",
            "date": "2026-03-30",
        },
        {
            "source": "TechCrunch",
            "title": "Another AI News",
            "url": "https://example.com/news2",
            "content": "",
            "summary": "Another summary",
            "score": 50,
            "icon": "",
            "date": "2026-03-30",
        },
    ]


@pytest.fixture
def sample_translation_input():
    """Sample input for translation."""
    return """HackerNews: 5 top posts
1. Title 1 - https://example.com/1
2. Title 2 - https://example.com/2
3. Title 3 - https://example.com/3
4. Title 4 - https://example.com/4
5. Title 5 - https://example.com/5"""