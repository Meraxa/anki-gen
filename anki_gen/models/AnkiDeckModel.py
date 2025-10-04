import uuid
import genanki
from pydantic import BaseModel, Field

from anki_gen.models.AnkiNoteModel import AnkiNoteModel


class AnkiDeckModel(BaseModel):
    deck_name: str = Field(...)
    guid: int = Field(default_factory=lambda: uuid.uuid4().int >> 72)
    notes: list[AnkiNoteModel] = []

    def to_deck(self, model: genanki.Model) -> genanki.Deck:
        deck = genanki.Deck(self.guid, self.deck_name)
        for note in self.notes:
            deck.add_note(note.to_note(model=model))
        return deck
