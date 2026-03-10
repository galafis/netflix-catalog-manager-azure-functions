"""Content recommendation engine using cosine similarity."""
import math
from typing import List, Dict, Tuple
from app.models import Content


class RecommendationEngine:
    """Collaborative filtering recommendation engine based on content features."""

    def __init__(self, contents: Dict[str, Content]):
        self.contents = contents

    def _build_feature_vector(self, content: Content) -> Dict[str, float]:
        """Build a feature vector from content attributes."""
        features: Dict[str, float] = {}
        for genre in content.genre:
            features[f"genre_{genre.lower()}"] = 1.0
        features[f"type_{content.content_type}"] = 1.0
        features["year_normalized"] = (content.year - 1990) / 40.0
        features["rating_normalized"] = content.rating / 10.0
        if content.director:
            features[f"director_{content.director.lower().replace(' ', '_')}"] = 1.0
        return features

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Calculate cosine similarity between two feature vectors."""
        all_keys = set(vec_a.keys()) | set(vec_b.keys())
        dot_product = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in all_keys)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot_product / (mag_a * mag_b)

    def recommend(self, content_id: str, top_n: int = 5) -> List[Tuple[Content, float]]:
        """Get top-N recommendations similar to a given content item."""
        if content_id not in self.contents:
            return []
        target = self.contents[content_id]
        target_vec = self._build_feature_vector(target)
        similarities = []
        for cid, content in self.contents.items():
            if cid == content_id:
                continue
            vec = self._build_feature_vector(content)
            sim = self._cosine_similarity(target_vec, vec)
            similarities.append((content, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]

    def recommend_by_genre(self, genre: str, top_n: int = 10) -> List[Content]:
        """Get top-rated content by genre."""
        results = [
            c for c in self.contents.values()
            if genre.lower() in [g.lower() for g in c.genre]
        ]
        results.sort(key=lambda x: x.rating, reverse=True)
        return results[:top_n]
