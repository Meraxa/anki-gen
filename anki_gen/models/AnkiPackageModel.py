import genanki
from pydantic import BaseModel

from anki_gen.models.AnkiDeckModel import AnkiDeckModel


class AnkiPackageModel(BaseModel):
    decks: list[AnkiDeckModel] = []
    media_files: list[str] = []

    def to_package(self, model: genanki.Model) -> genanki.Package:
        genanki_decks = [deck.to_deck(model=model) for deck in self.decks]
        return genanki.Package(genanki_decks, media_files=self.media_files)
