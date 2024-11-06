import os

from google.cloud import translate_v2  # type: ignore
from google.cloud.translate_v2 import Client  # type: ignore

from webscrapper.utils import Files


class Translator:

    def __init__(self, source: str, target: str) -> None:
        self.__source_language: str = source
        self.__target_language: str = target
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Files.create_path_inside("data\\google-translate-credentials.json")
        self.__client: Client = translate_v2.Client()

    @property
    def source(self) -> str:
        return self.__source_language

    @property
    def target(self) -> str:
        return self.__target_language

    def translate(self, text: str | bytes) -> str:

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result: dict = self.__client.translate(text, source_language=self.__source_language, target_language=self.__target_language)

        return result["translatedText"]
