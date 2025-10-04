from datetime import datetime, timezone
from typing import Literal, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class BaseLearningItemModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    guid: int = Field(default_factory=lambda: uuid.uuid4().int >> 72)
    created_at: str = Field(
        default=datetime.now(timezone.utc).astimezone().isoformat(),
        description="The creation date of the learning item.",
        examples=["2024-01-12T21:58:41.546469+01:00"],
    )
    updated_at: Optional[str] = Field(
        default=None,
        description="The last update date of the learning item.",
        examples=["2024-01-12T21:58:41.546469+01:00"],
    )
    language_level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = Field(
        default=None,
        description="The language level of the learning item.",
        examples=["A1"],
    )
    base_item: str = Field(
        ...,
        description="The learning item in the base language.",
        examples=["das Haus"],
    )
    target_item: str = Field(
        ...,
        description="The learning item in the learning language.",
        examples=["the house"],
    )
    base_item_audio_id: str = Field(
        ...,
        description="The ID of the audios that pronounce the base item.",
        examples=["658eb49d41d98125d5ad2b82"],
    )
    target_item_audio_id: str = Field(
        ...,
        description="The ID of the audios that pronounce the target item.",
        examples=["658eb49d41d98125d5ad2b82"],
    )
    image_id: str = Field(
        ...,
        description="The ID of the images that represent this sentence.",
        examples=["658eb49d41d98125d5ad2b82"],
    )
