import genanki
import pickle

from anki_gen.models.AnkiDeckModel import AnkiDeckModel
from anki_gen.models.AnkiNoteModel import AnkiNoteModel
from anki_gen.models.AnkiPackageModel import AnkiPackageModel
from anki_gen.models.VocabularyModel import VocabularyModel
from anki_gen.models.SentenceModel import SentenceModel


my_model = genanki.Model(
    1788678359,
    "Anki Gen Model",
    fields=[
        {"name": "Deck"},
        {"name": "VocabularyImage"},
        {"name": "BaseLanguageVocabulary"},
        {"name": "LearningLanguageVocabulary"},
        {"name": "LearningLanguageVocabularySound"},
        {"name": "SentenceImage"},
        {"name": "BaseLanguageSentence"},
        {"name": "LearningLanguageSentence"},
        {"name": "LearningLanguageSentenceSound"},
    ],
    templates=[
        {
            "name": "Word Card",
            "qfmt": '<div id="rubric">{{Deck}}</div>{{VocabularyImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{BaseLanguageVocabulary}}</div>',
            "afmt": '<div id="rubric">{{Deck}}</div>{{VocabularyImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{LearningLanguageVocabulary}}</div>{{LearningLanguageVocabularySound}}',
        },
        {
            "name": "Word Card Reverse",
            "qfmt": '<div id="rubric">{{Deck}}</div>{{VocabularyImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{LearningLanguageVocabulary}}</div>{{LearningLanguageVocabularySound}}',
            "afmt": '<div id="rubric">{{Deck}}</div>{{VocabularyImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{BaseLanguageVocabulary}}</div>',
        },
        {
            "name": "Sentence Card",
            "qfmt": '<div id="rubric">{{Deck}}</div>{{SentenceImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{LearningLanguageSentence}}</div>{{LearningLanguageSentenceSound}}',
            "afmt": '<div id="rubric">{{Deck}}</div>{{SentenceImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{BaseLanguageSentence}}</div>',
        },
        {
            "name": "Sentence Card Reverse",
            "qfmt": '<div id="rubric">{{Deck}}</div>{{SentenceImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{LearningLanguageSentence}}</div>{{LearningLanguageSentenceSound}}',
            "afmt": '<div id="rubric">{{Deck}}</div>{{SentenceImage}}<div style="font-family: Arial; font-size: 70px;color:#FF80DD;">{{BaseLanguageSentence}}</div>',
        },
    ],
    css="""
        .card {
            font-family: arial;
            font-size:150%;
            text-align: center;
            color: Black;
            background-color:black;
        }

        #rubric {
            text-align: left;
            padding: 4px;
            padding-left: 10px;
            padding-right: 10px;
            margin-bottom: 10px;
            background: #1d6695;
            color: white;
            font-weight: 500;
        }

        img{
            max-width:100%;
            height:auto;
                width:300px;
                border-radius: 20px;
        }
    """,
)

vocabulary_1 = VocabularyModel(
    language_level="A1",
    base_item="das Haus",
    target_item="the house",
    base_item_audio_id="658eb49d41d98125d5ad2b82",
    target_item_audio_id="658eb49d41d98125d5ad2b82",
    image_id="658eb49d41d98125d5ad2bq2",
    type="noun",
)

sentence_1 = SentenceModel(
    language_level="A1",
    base_item="Das Haus ist groß.",
    target_item="The house is big.",
    base_item_audio_id="658eb49d41d98125d5ad2b82",
    target_item_audio_id="658eb49d41d98125d5ad2b82",
    image_id="658eb49d41d98125d5ad2bq2",
    type="statement",
)

note = AnkiNoteModel(
    deck_name="Anki Gen::Swimming",
    vocabulary=vocabulary_1,
    sentence=sentence_1,
)

deck = AnkiDeckModel(
    deck_name="Anki Gen::Swimming",
    notes=[note],
)

package = AnkiPackageModel(
    decks=[deck],
    media_files=[],
)

with open("package.json", "w") as f:
    f.write(package.model_dump_json(indent=4))

with open("deck.pkl", "wb") as f:
    pickle.dump(package, f)
    pack = package.to_package(model=my_model)
    pack.write_to_file("package.apkg")

package = None

with open("deck.pkl", "rb") as f:
    package: AnkiPackageModel = pickle.load(f)

package.decks[0].notes[0].vocabulary.target_item = "the building"

vocabulary_2 = VocabularyModel(
    language_level="A1",
    base_item="tauchen",
    target_item="to dive",
    base_item_audio_id="658eb49d41d98125d5ad2b83",
    target_item_audio_id="658eb49d41d98125d5ad2b83",
    image_id="658eb49d41d98125d5ad2bq3",
    type="verb",
)

sentence_2 = SentenceModel(
    language_level="A1",
    base_item="Am Montag tauchen wir im See.",
    target_item="On Monday we dive in the lake.",
    base_item_audio_id="658eb49d41d98125d5ad2b83",
    target_item_audio_id="658eb49d41d98125d5ad2b83",
    image_id="658eb49d41d98125d5ad2bq3",
    type="statement",
)

note = AnkiNoteModel(
    deck_name="Anki Gen",
    vocabulary=vocabulary_2,
    sentence=sentence_2,
)

package.decks[0].notes.append(note)
pack = package.to_package(model=my_model)
pack.write_to_file("package.apkg")
exit()
