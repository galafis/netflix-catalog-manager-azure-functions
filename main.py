"""Netflix Catalog Manager - Demo Entry Point."""
from app.database import ContentDatabase
from app.services.recommender import RecommendationEngine


def main():
    """Run catalog manager demo."""
    db = ContentDatabase()
    recommender = RecommendationEngine(db.contents)

    print("Netflix Catalog Manager")
    print("=" * 60)
    print(f"Total content items: {len(db.contents)}")
    print(f"Available genres: {', '.join(db.get_genres())}")
    print()

    # List all content
    all_content = db.list_all()
    print("All Content:")
    for c in all_content:
        print(f"  [{c.content_type.upper():12s}] {c.title} ({c.year}) - {c.rating}/10")
    print()

    # Search by genre
    sci_fi = db.search(genre="Sci-Fi")
    print(f"Sci-Fi titles ({len(sci_fi)}):")
    for c in sci_fi:
        print(f"  - {c.title} ({c.year}) - {c.rating}/10")
    print()

    # Search by text
    results = db.search(query="dream")
    print(f"Search 'dream' ({len(results)} results):")
    for c in results:
        print(f"  - {c.title}: {c.description[:60]}...")
    print()

    # Recommendations
    sample = all_content[0]
    recs = recommender.recommend(sample.id, top_n=5)
    print(f"Recommendations similar to '{sample.title}':")
    for content, score in recs:
        print(f"  - {content.title} (similarity: {score:.3f})")
    print()

    # Genre recommendations
    top_drama = recommender.recommend_by_genre("Drama", top_n=5)
    print("Top Drama titles:")
    for c in top_drama:
        print(f"  - {c.title} ({c.year}) - {c.rating}/10")


if __name__ == "__main__":
    main()
