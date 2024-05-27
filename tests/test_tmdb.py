from unittest.mock import Mock
from tmdb_client import call_tmdb_api, get_single_movie, get_poster_url, get_single_movie_cast
import requests


def mock_call_tmdb_api(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('tmdb_client.call_tmdb_api', mock)
    return mock

def test_call_tmdb_api(monkeypatch):
    def mock_get(url, headers):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"key": "value"}
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    endpoint = "test_endpoint"
    result = call_tmdb_api(endpoint)
    assert result == {"key": "value"}

def test_get_single_movie(monkeypatch):
    def mock_call_tmdb_api(endpoint):
         return {"id": 1, "title": "Test Movie"}

    monkeypatch.setattr('tmdb_client.call_tmdb_api', mock_call_tmdb_api)

    movie_id = 1
    result = get_single_movie(movie_id)
    assert result == {"id": 1, "title": "Test Movie"}

def test_get_poster_url():
    poster_api_path = "test_poster.jpg"
    size = "w342"
    result = get_poster_url(poster_api_path, size)
    assert result == f"https://image.tmdb.org/t/p/{size}/{poster_api_path}"

def test_get_single_movie_cast(monkeypatch):
    def mock_call_tmdb_api(endpoint):
         return [{"id": 1, "name": "Actor 1"}, {"id": 2, "name": "Actor 2"}]

    monkeypatch.setattr('tmdb_client.call_tmdb_api', mock_call_tmdb_api)

    movie_id = 1
    result = get_single_movie_cast(movie_id)
    assert result == [{"id": 1, "name": "Actor 1"}, {"id": 2, "name": "Actor 2"}]
