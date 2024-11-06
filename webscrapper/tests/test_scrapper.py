from typing import List
import unittest

from webscrapper.scrapper import Scrapper, Tag, ResultSet, Content


class ScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        source_code: str = """
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>My Website</title>
                <!-- Additional metadata, stylesheets, or scripts can be included here -->
            </head>

            <body>
                <header>
                    <!-- Site header content goes here -->
                </header>
                <main>
                    <h1>MY TITLE</h1>
                    <div class="container">
                        I'm a text on a sample website. This is a<br>break.
                        <p>
                            <em>The first text.</em>
                            Chemistry has formulas H<sub>2</sub>O.
                            Math has formulas x<sup>2</sup>.
                        </p>
                        Second text.
                        <p class="a b">
                            This <i>text</i> with a <a class="a c" href="about:blank" target="_blank">link</a> that can redirect you
                            to some cool website.
                        </p>
                        <p class="a c">
                            Text <strong>without</strong> link.
                        </p>
                        <video id="video" src="https://videos.pexels.com/video-files/28348416/12364336_2560_1440_24fps.mp4"
                            controls="controls" width="600">
                            Text inside video tag.
                        </video>
                        <hr>
                        <code>Monospaced font on code tag</code> before an <blockquote>interesting quote</blockquote>.
                        <strong>Bold text is stronger!</strong>
                        Outsider <b>text</b>.
                        <img title="Sea lion" src="https://picsum.photos/200/300?grayscale" alt="B&W image" />
                    </div>
                </main>
                <footer>
                    <!-- Site footer content goes here -->
                </footer>
                <script src="index.js"></script>
            </body>

            </html>
            """

        self.simple_source_code: str = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                </head>
                <body>
                </body>
            </html>
        """

        self.scrapper: Scrapper = Scrapper(source_code)
        return super().setUp()

    @unittest.skip("Success")
    def test_delete_tags(self) -> None:
        self.scrapper.delete_tags(["head"])
        self.scrapper.print_source_code()

    @unittest.skip("Success")
    def test_has_source_code(self) -> None:
        self.assertTrue(self.scrapper.has_source_code())
        self.scrapper.set_source_code("")
        self.assertTrue(not self.scrapper.has_source_code())

    @unittest.skip("Success")
    def test_set_source_code(self) -> None:
        self.scrapper.set_source_code(self.simple_source_code)
        self.scrapper.print_source_code()

    @unittest.skip("Success")
    def test_set_root(self) -> None:
        p: Tag | None =self.scrapper.find_one("p", "")
        if p:
            self.scrapper.set_root(p)
        self.scrapper.print_source_code()

    @unittest.skip("Success")
    def test_find_all(self) -> None:
        p_none: List = self.scrapper.find_all("p", recursive=False)

        self.assertEqual(p_none, [])

        p_list: ResultSet[Tag] = self.scrapper.find_all("p")

        self.assertEqual(len(p_list), 3)

        pa_list: ResultSet[Tag] = self.scrapper.find_all("p", "a")

        self.assertEqual(len(pa_list), 2)

        for pa in pa_list:
            print(pa.text.strip())

    @unittest.skip("Success")
    def test_find_one(self) -> None:
        p_none: Tag | None = self.scrapper.find_one("p", recursive=False)

        self.assertEqual(p_none, None)

        p: Tag | None = self.scrapper.find_one("p")
        if p:
            self.assertEqual(p.text.strip(), "The first text")
            div: Tag | None = self.scrapper.find_one("div", "container")
            if div:
                p_on_div: Tag | None = self.scrapper.find_one("p", element=div)
                if p_on_div:
                    self.assertTrue(p.text == p_on_div.text)

        pb: Tag | None = self.scrapper.find_one("p", "b")
        pab: Tag | None = self.scrapper.find_one("p", "a b")
        self.assertTrue(pb == pab)

        pc: Tag | None = self.scrapper.find_one("p", "c")
        pac: Tag | None = self.scrapper.find_one("p", "a c")
        self.assertTrue(pc == pac)

    @unittest.skip("Success")
    def test_get_content(self) -> None:
        main: Tag | None = self.scrapper.find_one("main")

        if main:
            content: Content = self.scrapper.get_content(main)

        print(f"\n{content.text}")
