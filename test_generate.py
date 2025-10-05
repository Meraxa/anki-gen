import base64
import uuid
from io import BytesIO
from typing import Literal

from openai import OpenAI
from PIL import Image
from pydantic import BaseModel, Field
from anki_gen.models.AnkiDeckModel import AnkiDeckModel
from anki_gen.models.AnkiNoteModel import AnkiNoteModel
from anki_gen.models.AnkiPackageModel import AnkiPackageModel
from anki_gen.models.SentenceModel import SentenceModel
from anki_gen.models.VocabularyModel import VocabularyModel
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAPI_KEY", ""))


class PromptModel(BaseModel):
    base_item: str
    target_item: str


class VocabularyPromptModel(PromptModel):
    base_item: str = Field(
        ...,
        description="The learning item in the base language.",
        examples=["das Haus"],
    )
    target_item: str = Field(
        ...,
        description="The learning item in the learning language.",
        examples=(["the house"],),
    )
    type: Literal["verb", "adjective", "noun", "adverb"] = Field(
        ..., description="The type of the word.", examples=["noun"]
    )


class VocabularySet(BaseModel):
    vocabularies: list[VocabularyPromptModel]


class SentencePromptModel(PromptModel):
    base_item: str = Field(
        ...,
        description="The sentence in the base language.",
    )
    target_item: str = Field(
        ...,
        description="The sentence in the learning language.",
    )
    type: Literal["question", "statement"] = Field(
        ..., description="The type of the sentence.", examples=["statement"]
    )


def call_audio_api(input_value: str):
    audio_uid = uuid.uuid4().int >> 72
    openai_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_value,
    )
    openai_response.write_to_file(f"data/sounds/{audio_uid}.mp3")
    return audio_uid


def generate_audio(item: PromptModel):
    base_audio_uid = call_audio_api(item.base_item)
    target_audio_uid = call_audio_api(item.target_item)
    return base_audio_uid, target_audio_uid


def generate_image(
    motive: str,
    topic: str,
):
    image_uid = uuid.uuid4().int >> 72
    # https://community.openai.com/t/howto-use-the-new-python-library-to-call-api-dall-e-and-save-and-display-images/495741

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"A image representing a realistic example of the sentence or vocabulary '{motive}' for the topic '{topic}'.",
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",
    )

    data = response.data[0].model_dump().get("b64_json")
    image = Image.open(BytesIO(base64.b64decode(data)))
    image.save(f"data/images/{image_uid}.png")
    return image_uid


def generate(topic: str, language_level: Literal["A1", "A2", "B1", "B2", "C1", "C2"]):
    # Generate vocabularies
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a vocabulary generator used to generate a set of 5 vocabularies for the given topic and the languages.",
            },
            {
                "role": "user",
                "content": f"Create a vocabulary set for the topic '{topic}'. Language Level: {language_level}. Target language: {'English'}. Base language: {'German'}.",
            },
        ],
        response_format=VocabularySet,
    )
    generated_vocabularies = completion.choices[0].message.parsed.vocabularies

    # Generate sentences for the vocabularies
    anki_notes: list[AnkiNoteModel] = []
    for vocabulary in generated_vocabularies:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentence generator used to generate a sentence for the given vocabulary, topic, language level and languages. Pay special attention to the grammar.",
                },
                {
                    "role": "user",
                    "content": f"Create a sentence for the vocabulary '{vocabulary.target_item}' in the scope of the topic '{topic}'. Language Level: {language_level}.  Target language: {'English'}. Base language: {'German'}.",
                },
            ],
            response_format=SentencePromptModel,
        )
        generated_sentence = completion.choices[0].message.parsed

        # Generate Audio and Image for the vocabulary and sentence
        vocabulary_base_audio_id, vocabulary_target_audio_id = generate_audio(
            vocabulary
        )
        vocabulary_image_id = generate_image(vocabulary.target_item, topic=topic)
        generated_base_sentence_audio_id, generated_target_sentence_audio_id = (
            generate_audio(generated_sentence)
        )
        generated_sentence_image_id = generate_image(
            generated_sentence.target_item, topic=topic
        )

        anki_notes.append(
            AnkiNoteModel(
                deck_name=f"Anki Gen::{topic}",
                vocabulary=VocabularyModel(
                    language_level=language_level,
                    base_item=vocabulary.base_item,
                    target_item=vocabulary.target_item,
                    type=vocabulary.type,
                    base_item_audio_id=vocabulary_base_audio_id,
                    target_item_audio_id=vocabulary_target_audio_id,
                    image_id=vocabulary_image_id,
                ),
                sentence=SentenceModel(
                    language_level=language_level,
                    base_item=generated_sentence.base_item,
                    target_item=generated_sentence.target_item,
                    type=generated_sentence.type,
                    base_item_audio_id=generated_base_sentence_audio_id,
                    target_item_audio_id=generated_target_sentence_audio_id,
                    image_id=generated_sentence_image_id,
                ),
            )
        )
    deck = AnkiDeckModel(
        deck_name="Anki Gen::Swimming",
        notes=anki_notes,
    )
    package = AnkiPackageModel(
        decks=[deck],
        media_files=[],
    )
    with open("generate_package.json", "w") as f:
        f.write(package.model_dump_json(indent=4))


generate(topic="Swimming", language_level="A1")
