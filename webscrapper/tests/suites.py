from unittest import TestSuite, TextTestRunner

from test_browser import BrowserTest # type: ignore
# from test_scrapper import ScrapperTest
# from test_translator import TranslatorTest
# from test_utils import UtilsTest

def browser_suite() -> TestSuite:
    suite = TestSuite()

    suite.addTest(BrowserTest("test_go_to_url_blank_page"))
    suite.addTest(BrowserTest("test_go_to_url_sample_page"))
    suite.addTest(BrowserTest("test_get_page_title"))
    suite.addTest(BrowserTest("test_get_source_code"))
    suite.addTest(BrowserTest("test_close_tab"))
    suite.addTest(BrowserTest("test_go_and_close_tab"))
    suite.addTest(BrowserTest("test_wait_and_find_on_element_by_class"))
    suite.addTest(BrowserTest("test_wait_and_find_one_by_class"))
    suite.addTest(BrowserTest("test_wait_and_find_on_element_by_tag"))
    suite.addTest(BrowserTest("test_wait_and_find_one_by_tag"))
    suite.addTest(BrowserTest("test_wait_and_find_on_element_by_css"))
    suite.addTest(BrowserTest("test_wait_and_find_one_by_css"))
    suite.addTest(BrowserTest("test_wait_and_find_on_element_by_xpath"))
    suite.addTest(BrowserTest("test_wait_and_find_one_by_xpath"))

    return suite

if __name__ == "main":
    runner = TextTestRunner()
    runner.run(browser_suite())
