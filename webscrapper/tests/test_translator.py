import unittest

from webscrapper.translator import Translator


class TranslatorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.translator: Translator = Translator("es","en")
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @unittest.skip("Success")
    def test_translate(self):
        text = "Hola, soy un abanico de techo"

        translation = self.translator.translate(text)

        print(translation)
