import uuid
import genanki
from pydantic import BaseModel, ConfigDict, Field

from anki_gen.models.SentenceModel import SentenceModel
from anki_gen.models.VocabularyModel import VocabularyModel


class AnkiNoteModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vocabulary: VocabularyModel = Field(...)
    sentence: SentenceModel = Field(...)
    deck_name: str = Field(...)
    guid: int = Field(default_factory=lambda: uuid.uuid4().int >> 72)

    def to_note(self, model: genanki.Model) -> genanki.Note:
        return genanki.Note(
            model=model,
            fields=[
                self.deck_name,
                f'<img src="{self.vocabulary.image_id}.jpg">',
                self.vocabulary.base_item,
                self.vocabulary.target_item,
                f"[sound:{self.vocabulary.target_item_audio_id}.mp3]",
                f'<img src="{self.sentence.image_id}.jpg">',
                self.sentence.base_item,
                self.sentence.target_item,
                f"[sound:{self.sentence.target_item_audio_id}.mp3]",
            ],
            guid=self.guid,
        )
