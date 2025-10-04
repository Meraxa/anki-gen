from typing import Literal

from pydantic import Field

from anki_gen.models.BaseLearningItemModel import BaseLearningItemModel


class VocabularyModel(BaseLearningItemModel):
    type: Literal["verb", "adjective", "noun", "adverb"] = Field(
        ..., description="The type of the word.", examples=["noun"]
    )
