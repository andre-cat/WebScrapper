import os
from typing import List
import unittest
from unittest import TestCase

from webscrapper.browser import Browser, WebElement
from webscrapper.utils import Files


class BrowserTest(TestCase):

    def setUp(self) -> None:
        self.browser: Browser = Browser()
        return super().setUp()

    def tearDown(self) -> None:
        source_code_path: str = Files.create_path_outside("source-code.html")

        if os.path.exists(source_code_path):
            os.remove(source_code_path)

        return super().tearDown()

    @unittest.skip("Success")
    def test_go_to_url_blank_page(self) -> None:
        link: str = "about:blank"

        self.browser.go_to_url(link)

        self.browser.quit()

    @unittest.skip("Success")
    def test_go_to_url_sample_page(self) -> None:
        link: str = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.browser.quit()

    @unittest.skip("Success")
    def test_get_page_title(self) -> None:
        link: str = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.assertEqual(self.browser.get_page_title(), "Google", "Page has not loading correctly")

        self.browser.quit()

    @unittest.skip("Success")
    def test_get_source_code(self) -> None:
        link: str = "https://www.google.com/"

        self.browser.go_to_url(link, 5)

        Files.create_file("source-code.html", self.browser.get_page_source_code())

        self.browser.quit()

    @unittest.skip("Success")
    def test_close_tab(self) -> None:

        self.browser.go_to_url("https://doodles.google/doodle/celebrating-oskar-picht/")
        print(self.browser.get_page_title())

        self.browser.open_tab("https://doodles.google/doodle/celebrating-popcorn/")
        self.browser.go_to_tab(2)

        self.browser.open_tab("https://doodles.google/doodle/saudi-arabia-national-day-2024/")
        self.browser.close_tab(3)
        print(self.browser.get_page_title())

        self.browser.close_tab()
        print(self.browser.get_page_title())

        self.browser.close_tab()

    @unittest.skip("Success")
    def test_go_and_close_tab(self) -> None:

        self.browser.go_to_url()

        page_title: str

        self.browser.open_tab("https://doodles.google/doodle/celebrating-oskar-picht/")
        self.browser.go_to_tab(2)
        page_title = self.browser.get_page_title()
        assert page_title == "Celebrating Oskar Picht Doodle - Google Doodles"

        self.browser.open_tab("https://doodles.google/doodle/celebrating-popcorn/")
        self.browser.go_to_tab(3)
        page_title = self.browser.get_page_title()
        assert page_title == "Celebrating Popcorn Doodle - Google Doodles"

        self.browser.open_tab("https://doodles.google/doodle/saudi-arabia-national-day-2024/")
        self.browser.go_to_tab(4)
        page_title = self.browser.get_page_title()
        assert page_title == "Saudi Arabia National Day 2024 Doodle - Google Doodles"

        self.browser.close_tab(2)
        self.browser.go_to_tab(2)
        page_title = self.browser.get_page_title()
        assert page_title == "Celebrating Popcorn Doodle - Google Doodles"

        self.browser.close_tab()
        self.browser.go_to_tab(2)
        page_title = self.browser.get_page_title()
        assert page_title == "Saudi Arabia National Day 2024 Doodle - Google Doodles"

    @unittest.skip("Success")
    def test_wait_and_find_on_element_by_class(self) -> None:
        link: str = "https://doodles.google/"

        self.browser.go_to_url(link, 5)

        self.browser.wait_class_present("doodle-card-wrapper")

        doodles: List[WebElement] = self.browser.find_by_class("doodle-card-wrapper")

        for doodle in doodles:
            doodle_title: WebElement | None = self.browser.find_one_by_class("doodle-card-content__event", doodle)

            if doodle_title:
                print("Doodle title:", doodle_title.text)

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_one_by_class(self) -> None:
        link: str = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.browser.wait_class_present("gNO89b")

        search_button: WebElement | None = self.browser.find_one_by_class("gNO89b")

        button_text: str

        if search_button:
            button_text = search_button.get_attribute("aria-label") or ""

        self.assertEqual(button_text, "Buscar con Google", "Element has not been found by class")

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_on_element_by_tag(self) -> None:
        link: str = "https://doodles.google/"

        self.browser.go_to_url(link, 5)

        self.browser.wait_class_present("color-picker")

        picker_element: WebElement | None = self.browser.find_one_by_class("color-picker")

        if picker_element:

            colors: List[WebElement] = self.browser.find_by_tag("path", element=picker_element)

            for color in colors:
                color_name: str = color.get_attribute("data-color") or ""
                print("Color name:", color_name)

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_one_by_tag(self) -> None:
        link = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.browser.wait_tag_present("a")

        gmail_link: WebElement | None = self.browser.find_one_by_tag("a")

        link_text: str

        if gmail_link:
            link_text = gmail_link.get_attribute("aria-label") or ""

        self.assertEqual(link_text, "Gmail", "Element has not been found by tag")

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_on_element_by_css(self) -> None:
        link: str = "https://doodles.google/"

        self.browser.go_to_url(link, 5)

        self.browser.wait_css_present(".glue-carousel__list")

        doodles_parent: WebElement | None = self.browser.find_one_by_css(".glue-carousel__list")

        if doodles_parent:

            doodles: List[WebElement] = self.browser.find_by_css(".doodle-card")

            for doodle in doodles:
                doodle_title: WebElement | None = self.browser.find_one_by_css(".doodle-card-content__event", doodle)

                if doodle_title:
                    print("Doodle title:", doodle_title.text)

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_one_by_css(self) -> None:
        link = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.browser.wait_css_present(".lnXdpd")

        gmail_link: WebElement | None = self.browser.find_one_by_css(".lnXdpd")

        link_text: str

        if gmail_link:
            link_text = gmail_link.get_attribute("alt") or ""

        self.assertEqual(link_text, "Google", "Element has not been found by css")

        self.browser.quit()

    @unittest.skip("FAILURE")
    def test_wait_and_find_on_element_by_xpath(self) -> None:
        link: str = "https://doodles.google/"

        self.browser.go_to_url(link, 5)

        self.browser.wait_xpath_present("//div[@class='mapChart']//circle")

        circles: List[WebElement] = self.browser.find_by_xpath("//div[@class='mapChart']//circle")

        for circle in circles:
            print("x", circle.get_attribute("cx"), "y", circle.get_attribute("cy"))

        self.browser.quit()

    @unittest.skip("Success")
    def test_wait_and_find_one_by_xpath(self) -> None:
        link = "https://www.google.com/"

        self.browser.go_to_url(link)

        self.browser.wait_xpath_present("//img[@class='lnXdpd']")

        gmail_link: WebElement | None = self.browser.find_one_by_xpath("//img[@class='lnXdpd']")

        link_text: str

        if gmail_link:
            link_text = gmail_link.get_attribute("alt") or ""

        self.assertEqual(link_text, "Google", "Element has not been found by xpath")

        self.browser.quit()
