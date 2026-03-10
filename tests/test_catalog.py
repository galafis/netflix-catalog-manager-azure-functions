"""Tests for the content catalog system."""
import pytest
from app.models import Content
from app.database import ContentDatabase
from app.services.recommender import RecommendationEngine


class TestContent:
    def test_create_content(self):
        c = Content("Test Movie", "movie", ["Action"], 2023, 8.0, 120, "A test movie.")
        assert c.title == "Test Movie"
        assert c.content_type == "movie"
        assert c.rating == 8.0
        assert len(c.id) > 0

    def test_to_dict(self):
        c = Content("Test", "series", ["Drama"], 2020, 7.5, 60, "Test series.")
        d = c.to_dict()
        assert d["title"] == "Test"
        assert d["content_type"] == "series"
        assert "id" in d
        assert "created_at" in d

    def test_content_with_cast(self):
        c = Content("Film", "movie", ["Action"], 2022, 8.5, 150, "Action film.",
                     cast=["Actor A", "Actor B"], director="Director X")
        assert len(c.cast) == 2
        assert c.director == "Director X"


class TestContentDatabase:
    def setup_method(self):
        self.db = ContentDatabase()

    def test_demo_data_loaded(self):
        assert len(self.db.contents) >= 10

    def test_create_content(self):
        c = Content("New Movie", "movie", ["Comedy"], 2024, 7.0, 90, "A comedy.")
        result = self.db.create(c)
        assert result.title == "New Movie"
        assert self.db.get(c.id) is not None

    def test_get_content(self):
        items = self.db.list_all(limit=1)
        content = self.db.get(items[0].id)
        assert content is not None
        assert content.title == items[0].title

    def test_get_nonexistent(self):
        assert self.db.get("nonexistent") is None

    def test_list_all(self):
        items = self.db.list_all()
        assert len(items) >= 10

    def test_list_with_pagination(self):
        page1 = self.db.list_all(limit=5, offset=0)
        page2 = self.db.list_all(limit=5, offset=5)
        assert len(page1) == 5
        assert len(page2) >= 1
        assert page1[0].id != page2[0].id

    def test_update_content(self):
        items = self.db.list_all(limit=1)
        updated = self.db.update(items[0].id, {"rating": 9.9})
        assert updated is not None
        assert updated.rating == 9.9

    def test_update_nonexistent(self):
        result = self.db.update("nonexistent", {"rating": 5.0})
        assert result is None

    def test_delete_content(self):
        c = Content("To Delete", "movie", ["Horror"], 2023, 5.0, 90, "Delete me.")
        self.db.create(c)
        assert self.db.delete(c.id) is True
        assert self.db.get(c.id) is None

    def test_delete_nonexistent(self):
        assert self.db.delete("nonexistent") is False

    def test_search_by_query(self):
        results = self.db.search(query="matrix")
        assert len(results) >= 1
        assert any("Matrix" in c.title for c in results)

    def test_search_by_genre(self):
        results = self.db.search(genre="Sci-Fi")
        assert len(results) >= 3
        for c in results:
            assert "Sci-Fi" in c.genre

    def test_search_by_type(self):
        results = self.db.search(content_type="documentary")
        assert len(results) >= 1
        for c in results:
            assert c.content_type == "documentary"

    def test_search_by_min_rating(self):
        results = self.db.search(min_rating=9.0)
        for c in results:
            assert c.rating >= 9.0

    def test_search_combined(self):
        results = self.db.search(genre="Sci-Fi", min_rating=8.5)
        for c in results:
            assert "Sci-Fi" in c.genre
            assert c.rating >= 8.5

    def test_get_genres(self):
        genres = self.db.get_genres()
        assert len(genres) >= 5
        assert "Sci-Fi" in genres
        assert "Drama" in genres


class TestRecommendationEngine:
    def setup_method(self):
        self.db = ContentDatabase()
        self.recommender = RecommendationEngine(self.db.contents)

    def test_recommend_returns_results(self):
        sample_id = list(self.db.contents.keys())[0]
        recs = self.recommender.recommend(sample_id, top_n=5)
        assert len(recs) <= 5
        assert len(recs) >= 1

    def test_recommend_excludes_self(self):
        sample_id = list(self.db.contents.keys())[0]
        recs = self.recommender.recommend(sample_id)
        for content, _ in recs:
            assert content.id != sample_id

    def test_recommend_similarity_scores(self):
        sample_id = list(self.db.contents.keys())[0]
        recs = self.recommender.recommend(sample_id)
        for _, score in recs:
            assert 0.0 <= score <= 1.0

    def test_recommend_sorted_by_similarity(self):
        sample_id = list(self.db.contents.keys())[0]
        recs = self.recommender.recommend(sample_id)
        scores = [s for _, s in recs]
        assert scores == sorted(scores, reverse=True)

    def test_recommend_nonexistent(self):
        recs = self.recommender.recommend("nonexistent")
        assert recs == []

    def test_recommend_by_genre(self):
        recs = self.recommender.recommend_by_genre("Drama", top_n=5)
        assert len(recs) >= 1
        for c in recs:
            assert "Drama" in c.genre

    def test_recommend_by_genre_sorted(self):
        recs = self.recommender.recommend_by_genre("Sci-Fi")
        ratings = [c.rating for c in recs]
        assert ratings == sorted(ratings, reverse=True)
