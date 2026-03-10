"""In-memory content database with search and filtering."""
from typing import List, Optional, Dict
from app.models import Content


class ContentDatabase:
    """In-memory content catalog database."""

    def __init__(self):
        self.contents: Dict[str, Content] = {}
        self._load_demo_data()

    def _load_demo_data(self):
        demo_data = [
            ("The Matrix", "movie", ["Sci-Fi", "Action"], 1999, 8.7, 136,
             "A hacker discovers reality is simulated.", ["Keanu Reeves", "Laurence Fishburne"], "Wachowskis"),
            ("Breaking Bad", "series", ["Drama", "Crime"], 2008, 9.5, 3000,
             "A chemistry teacher turns to drug manufacturing.", ["Bryan Cranston", "Aaron Paul"], "Vince Gilligan"),
            ("Inception", "movie", ["Sci-Fi", "Thriller"], 2010, 8.8, 148,
             "A thief enters dreams to plant ideas.", ["Leonardo DiCaprio", "Tom Hardy"], "Christopher Nolan"),
            ("Stranger Things", "series", ["Sci-Fi", "Horror"], 2016, 8.7, 2100,
             "Kids uncover supernatural mysteries.", ["Millie Bobby Brown"], "Duffer Brothers"),
            ("The Crown", "series", ["Drama", "History"], 2016, 8.6, 3600,
             "The reign of Queen Elizabeth II.", ["Claire Foy", "Olivia Colman"], "Peter Morgan"),
            ("Our Planet", "documentary", ["Nature", "Science"], 2019, 9.3, 400,
             "Exploration of natural wonders.", ["David Attenborough"], "Alastair Fothergill"),
            ("Interstellar", "movie", ["Sci-Fi", "Adventure"], 2014, 8.6, 169,
             "Explorers travel through a wormhole.", ["Matthew McConaughey"], "Christopher Nolan"),
            ("Dark", "series", ["Sci-Fi", "Mystery"], 2017, 8.8, 1560,
             "Time travel mysteries across generations.", ["Louis Hofmann"], "Baran bo Odar"),
            ("Parasite", "movie", ["Thriller", "Drama"], 2019, 8.5, 132,
             "A poor family infiltrates a wealthy household.", ["Song Kang-ho"], "Bong Joon-ho"),
            ("Money Heist", "series", ["Action", "Crime"], 2017, 8.2, 2400,
             "A mastermind plans the biggest heist.", ["Alvaro Morte"], "Alex Pina"),
            ("Cosmos", "documentary", ["Science", "Space"], 2014, 9.3, 780,
             "A journey through space and time.", ["Neil deGrasse Tyson"], "Brannon Braga"),
            ("The Witcher", "series", ["Fantasy", "Action"], 2019, 8.2, 960,
             "A monster hunter in a treacherous world.", ["Henry Cavill"], "Lauren Schmidt"),
            ("Pulp Fiction", "movie", ["Crime", "Drama"], 1994, 8.9, 154,
             "Interconnected stories of crime in LA.", ["John Travolta"], "Quentin Tarantino"),
            ("Black Mirror", "series", ["Sci-Fi", "Thriller"], 2011, 8.8, 1800,
             "Dark tales of technology impact.", ["Various"], "Charlie Brooker"),
            ("The Shawshank Redemption", "movie", ["Drama"], 1994, 9.3, 142,
             "Two imprisoned men find redemption.", ["Tim Robbins", "Morgan Freeman"], "Frank Darabont"),
        ]
        for title, ctype, genre, year, rating, dur, desc, cast, director in demo_data:
            c = Content(title, ctype, genre, year, rating, dur, desc, cast, director)
            self.contents[c.id] = c

    def create(self, content: Content) -> Content:
        self.contents[content.id] = content
        return content

    def get(self, content_id: str) -> Optional[Content]:
        return self.contents.get(content_id)

    def list_all(self, limit: int = 50, offset: int = 0) -> List[Content]:
        items = list(self.contents.values())
        return items[offset:offset + limit]

    def update(self, content_id: str, updates: dict) -> Optional[Content]:
        if content_id not in self.contents:
            return None
        content = self.contents[content_id]
        for key, value in updates.items():
            if hasattr(content, key) and key != "id":
                setattr(content, key, value)
        return content

    def delete(self, content_id: str) -> bool:
        return self.contents.pop(content_id, None) is not None

    def search(self, query: str = "", genre: str = "", year: int = 0,
               min_rating: float = 0, content_type: str = "") -> List[Content]:
        results = list(self.contents.values())
        if query:
            q = query.lower()
            results = [c for c in results if q in c.title.lower() or q in c.description.lower()]
        if genre:
            results = [c for c in results if genre.lower() in [g.lower() for g in c.genre]]
        if year:
            results = [c for c in results if c.year == year]
        if min_rating:
            results = [c for c in results if c.rating >= min_rating]
        if content_type:
            results = [c for c in results if c.content_type == content_type]
        return results

    def get_genres(self) -> List[str]:
        genres = set()
        for c in self.contents.values():
            genres.update(c.genre)
        return sorted(genres)
