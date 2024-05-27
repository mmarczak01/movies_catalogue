from main import app
from unittest.mock import Mock
from tmdb_client import get_single_movie, get_poster_url, get_single_movie_cast
import pytest

@pytest.mark.parametrize("list_type, expected_api_call", (
    ("popular", "movie/popular"),
    ("top_rated", "movie/top_rated"),
    ("now_playing", "movie/now_playing"),
    ("upcoming", "movie/upcoming")
))

def mock_call_tmdb_api(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('tmdb_client.call_tmdb_api', mock)
    return mock

def test_homepage(monkeypatch, list_type, expected_api_call):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(f'/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_once_with(expected_api_call)

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
