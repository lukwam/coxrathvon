"""Unit tests for the CoxRathvon Flask app."""

import os
import unittest
from unittest.mock import patch

# Set required env vars before importing main
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")

from app.main import (  # noqa: E402
    app,
    get_data,
    get_puzzle_by_id,
    get_puzzles_dict,
)


class TestFlaskApp(unittest.TestCase):
    """Test the Flask app routes."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Sample puzzle data
        self.sample_puzzles = [
            {
                "id": "atlantic-001",
                "title": "Short and Sweet",
                "date": "2024-01-15",
                "publication": "atlantic",
                "issue": "Atlantic #1",
                "number": "1",
                "year": 2024,
                "month": 1,
                "day": 15,
                "hexgrid": None,
            },
            {
                "id": "wsj-001",
                "title": "Wall Street Puzzle",
                "date": "2024-02-20",
                "publication": "wsj",
                "issue": None,
                "number": "42",
                "year": 2024,
                "month": 2,
                "day": 20,
                "hexgrid": None,
            },
        ]


class TestGetData(TestFlaskApp):
    """Tests for the get_data function."""

    @patch("app.main.shutil.copy")
    @patch(
        "builtins.open",
        unittest.mock.mock_open(read_data='[{"id": "test", "title": "Test"}]'),
    )
    @patch("app.main.os.path.isfile", return_value=False)
    def test_get_data_copies_file_when_missing(self, mock_isfile, mock_copy):
        """Test that get_data copies data.json to /tmp when missing."""
        result = get_data()
        mock_copy.assert_called_once_with("data.json", "/tmp/data.json")
        assert len(result) == 1
        assert result[0]["id"] == "test"

    @patch(
        "builtins.open",
        unittest.mock.mock_open(read_data='[{"id": "cached", "title": "Cached"}]'),
    )
    @patch("app.main.os.path.isfile", return_value=True)
    def test_get_data_uses_cached_file(self, mock_isfile):
        """Test that get_data uses the cached /tmp/data.json when present."""
        result = get_data()
        assert len(result) == 1
        assert result[0]["id"] == "cached"


class TestGetPuzzlesDict(TestFlaskApp):
    """Tests for the get_puzzles_dict function."""

    @patch("app.main.get_data")
    def test_get_puzzles_dict_by_id(self, mock_get_data):
        """Test getting puzzles indexed by id."""
        mock_get_data.return_value = self.sample_puzzles
        result = get_puzzles_dict()
        assert "atlantic-001" in result
        assert "wsj-001" in result
        assert result["atlantic-001"]["title"] == "Short and Sweet"

    @patch("app.main.get_data")
    def test_get_puzzles_dict_by_custom_key(self, mock_get_data):
        """Test getting puzzles indexed by a custom key."""
        mock_get_data.return_value = self.sample_puzzles
        result = get_puzzles_dict(key="publication")
        assert "atlantic" in result
        assert "wsj" in result


class TestGetPuzzleById(TestFlaskApp):
    """Tests for the get_puzzle_by_id function."""

    @patch("app.main.get_puzzles_dict")
    def test_get_puzzle_by_id_found(self, mock_dict):
        """Test getting a puzzle that exists."""
        mock_dict.return_value = {"atlantic-001": self.sample_puzzles[0]}
        result = get_puzzle_by_id("atlantic-001")
        assert result is not None
        assert result["title"] == "Short and Sweet"

    @patch("app.main.get_puzzles_dict")
    def test_get_puzzle_by_id_not_found(self, mock_dict):
        """Test getting a puzzle that doesn't exist."""
        mock_dict.return_value = {}
        result = get_puzzle_by_id("nonexistent")
        assert result is None


class TestRoutes(TestFlaskApp):
    """Tests for Flask routes."""

    @patch("app.main.get_data")
    def test_index_route(self, mock_get_data):
        """Test the index page renders successfully."""
        mock_get_data.return_value = self.sample_puzzles
        response = self.client.get("/")
        assert response.status_code == 200
        assert b"Short and Sweet" in response.data

    @patch("app.main.get_data")
    def test_index_sorted_by_date_descending(self, mock_get_data):
        """Test that index page shows puzzles in reverse chronological order."""
        mock_get_data.return_value = self.sample_puzzles
        response = self.client.get("/")
        data = response.data.decode()
        # The 2024-02-20 puzzle should appear before the 2024-01-15 puzzle
        wsj_pos = data.find("Wall Street Puzzle")
        atlantic_pos = data.find("Short and Sweet")
        assert wsj_pos < atlantic_pos

    @patch("app.main.get_puzzles_dict")
    def test_puzzle_page_not_found_redirects(self, mock_dict):
        """Test that a missing puzzle redirects to the index."""
        mock_dict.return_value = {}
        response = self.client.get("/puzzles/nonexistent")
        assert response.status_code == 302
        assert response.location == "/"

    @patch("app.main.get_puzzles_dict")
    def test_solution_not_found_redirects(self, mock_dict):
        """Test that a missing solution redirects to the index."""
        mock_dict.return_value = {}
        response = self.client.get("/solutions/nonexistent")
        assert response.status_code == 302
        assert response.location == "/"

    def test_static_script_route(self):
        """Test the script.js route."""
        response = self.client.get("/script.js")
        assert response.status_code == 200

    def test_static_style_route(self):
        """Test the style.css route."""
        response = self.client.get("/style.css")
        assert response.status_code == 200

    @patch("app.main.get_data")
    def test_data_json_route(self, mock_get_data):
        """Test the data.json route returns JSON."""
        response = self.client.get("/data.json")
        assert response.status_code == 200


class TestContextProcessor(TestFlaskApp):
    """Tests for the context processor."""

    @patch("app.main.get_data")
    def test_current_year_injected(self, mock_get_data):
        """Test that the current year is injected into templates."""
        mock_get_data.return_value = self.sample_puzzles
        import datetime

        response = self.client.get("/")
        assert str(datetime.datetime.now().year).encode() in response.data


if __name__ == "__main__":
    unittest.main()
