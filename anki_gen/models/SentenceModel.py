from typing import Literal

from pydantic import Field

from anki_gen.models.BaseLearningItemModel import BaseLearningItemModel


class SentenceModel(BaseLearningItemModel):
    type: Literal["statement", "question"] = Field(
        ..., description="The type of the sentence.", examples=["statement"]
    )
