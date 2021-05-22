import json
from os import path
from typing import Final, Optional

import pyaudio  # type: ignore
from vosk import KaldiRecognizer, Model  # type: ignore

from dao.sqlite_dao import SqliteDAO
from dispatcher.dispatcher import DispatchService
from helpers import config as config_helper
from listener.preprocessor import Preprocessor
from responder.responder import ResponseService
from speaker.speaker_ttsx3 import SpeakerTtsx3

#
# Settings
#


if (settings := config_helper.load_config()) is None:
    print("Fatal: Could not load configuration")
    exit(1)

#
# Validation
#


model_path: Final = path.join("vosk-models", "vosk-model-en-us-aspire-0.2")

if not path.exists(model_path):
    print(
        "Please download the model from https://alphacephei.com/vosk/models/vosk-model-en-us-aspire-0.2.zip"
    )
    exit(1)


#
# Initializing
#

print("Initializing speech to text model")

chunk_size: Final = 8000
audio_rate: Final = 16000

model: Final = Model(model_path)
recognizer: Final = KaldiRecognizer(model, audio_rate)

audio_client: Final = pyaudio.PyAudio()

stream = audio_client.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=audio_rate,
    input=True,
    frames_per_buffer=chunk_size,
)

print("Speech to text model ready")

print("Initializing database")

db: Final = SqliteDAO("food_log.db")

if not db.try_init_db_if_needed():
    print("Fatal: Could not init database")
    exit(1)

print("Initializing dispatcher")

speaker = SpeakerTtsx3(settings["speaking"]["message_patterns"])
dispatcher: Final = DispatchService(
    Preprocessor(settings["listening"]["replacements"]),
    ResponseService(db, speaker),
    settings["listening"]["keywords"],
    db.try_get_last_user_name(),
)

#
# Main loop
#

print("Everything ready")

while True:
    data = stream.read(int(chunk_size / 2), exception_on_overflow=False)

    if len(data) > 0 and recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        if "text" in result:
            print("I heard: " + result["text"])
            dispatcher.dispatch(result["text"])
