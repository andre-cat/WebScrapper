import time
from typing import Any, List

from selenium.common.exceptions import ElementNotInteractableException, JavascriptException, NoSuchElementException, NoSuchWindowException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from webscrapper.utils import Files, print_class_name


class Browser:

    @print_class_name
    def __init__(self) -> None:
        """
        Start a headless browser with options at chrome-options file.
        """
        try:
            print(f"Starting browser")

            options: Options = Options()

            for option in Files.read_file(Files.create_path_inside("data\\chrome-options.txt")):
                options.add_argument(option)

            options.add_experimental_option(
                "prefs",
                {"profile.cookie_controls_mode": 2, "profile.default_content_setting_values.cookies": 2, "profile.managed_default_content_settings.images": 2},
            )

            options.accept_insecure_certs = True
            options.browser_version = "stable"
            options.page_load_strategy = "eager"
            options.strict_file_interactability = True
            options.unhandled_prompt_behavior = "dismiss"

            binary_path: str = Files.create_path_inside("application\\chrome\\chrome_for_testing\\chrome.exe")
            options.binary_location = binary_path

            self.__options: Options = options

            driver_path: str = Files.create_path_inside("application\\chrome\\chrome_driver\\chromedriver.exe")
            self.__service: Service = Service(executable_path=driver_path)

            self.__driver: WebDriver = WebDriver(service=self.__service, options=self.__options)

        except WebDriverException as e:
            raise BrowserException(Browser, "Browser error at constructor", e)

    def get_page_source_code(self) -> str:
        """
        Return page source code.

        Returns:
            str
        """
        try:
            return self.__driver.page_source
        except WebDriverException as e:
            BrowserException.print_exception(self.get_page_source_code, f"Browser error getting page source code", e)
            return ""

    def get_page_title(self) -> str:
        """
        Return page title.

        Returns:
            str
        """
        try:
            return self.__driver.title
        except WebDriverException as e:
            BrowserException.print_exception(self.get_page_title, f"Browser error getting page title", e)
            return ""

    # @print_class_name
    def click_element(self, element: WebElement) -> None:
        """
        Perform the action click on a clickable element.

        Args:
            element (WebElement): element to be clicked
        """
        try:
            # print(f"Clicking element {element.tag_name}...")
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).click().perform()
        except ElementNotInteractableException as e:
            BrowserException.print_exception(self.click_element, f"Element {element.tag_name} is not interactable", e)

    # @print_class_name
    def set_attribute(self, element: WebElement, attribute: str, value: str) -> None:
        """
        Set the attribute of the given element.

        Args:
            element (WebElement): element to set attribute
            attribute (str): name of attribute
            value (str): value of attribtue
        """
        try:
            # print(f"Setting attribute {attribute} on element {element.tag_name}...")
            self.__driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", element, attribute, value)
        except JavascriptException as e:
            BrowserException.print_exception(self.click_element, f"It was not possible to set the attribute {attribute} on element {element.tag_name}", e)

    # @print_class_name
    def go_to_url(self, url: str = "about:blank", seconds: int = 0) -> None:
        """
        Go to url in the current tab.

        Args:
            url (str): url to go. about:blank by default
            seconds (int): waiting time for the page to load. 0 s by default
        """
        try:
            # print(f"Going to {url[0:50]}...")
            self.__driver.get(url)
            time.sleep(seconds)
        except WebDriverException as e:
            BrowserException.print_exception(self.go_to_url, f"Browser error going to URL {url[:50]}...", e)

    # @print_class_name
    def open_tab(self, url: str = "about:blank", seconds: int = 0) -> None:
        """
        Open a new tab at given url.

        Args:
            url (str): new tab url. about:blank by default
            seconds (int): waiting time for the page to load. 0 s by default
        """
        try:
            # print(f"Opening a new tab at {url[:50]}...")
            self.__driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(seconds)
        except JavascriptException as e:
            BrowserException.print_exception(self.open_tab, f"JS error opening tab at {url[:50]}...", e)

    # @print_class_name
    def go_to_tab(self, index: int, seconds: int = 0) -> None:
        """
        Go to tab at index.

        Args:
            index (int): tab index; first index = 1
            seconds (int): waiting time for the page to load. 0 s by default
        """
        try:
            if index > 0:
                # print(f"Going to tab {index}")
                self.__driver.switch_to.window(self.__driver.window_handles[index - 1])
                time.sleep(seconds)
        except NoSuchWindowException as e:
            BrowserException.print_exception(self.go_to_tab, f"Unable to go to tab {index}", e)

    # @print_class_name
    def close_tab(self, index: int | None = None) -> None:
        """
        Close current tab or tab at index.

        Args:
            index (int | None): tab index; first index = 1. None by default
        """
        try:
            # if len(self.__driver.window_handles) > 1:
            if not index:
                # print("Closing current tab")
                self.__driver.close()
                self.__driver.switch_to.window(self.__driver.window_handles[-1])
            # elif index <= 0:
            # raise WebDriverException("Index must be greater than 0")
            else:
                # print(f"Closing tab {index}")
                current_handle: str = self.__driver.current_window_handle
                self.__driver.switch_to.window(self.__driver.window_handles[index - 1])
                self.__driver.close()
                self.__driver.switch_to.window(current_handle)
            # else:
            # raise WebDriverException("Remaining window can't be closed")
        except WebDriverException as e:
            BrowserException.print_exception(self.close_tab, f"Browser error closing tab {index}", e)

    # @print_class_name
    def delete_scripts(self) -> None:
        """
        Delete scripts at the current page.
        """
        try:
            # print(f"Deleting scripts...")
            deletion_code: str = """
                    (() => {
                        let scripts = document.getElementsByTagName('script');
                        for (var i = 0; i < scripts.length; i++) {
                            scripts[i].parentNode.removeChild(scripts[i]);
                        }
                        return scripts.length > 0
                    })()
                """
            page_has_scripts: bool = True

            while page_has_scripts:
                page_has_scripts = self.__driver.execute_script(deletion_code)
                time.sleep(1)
        except JavascriptException as e:
            BrowserException.print_exception(self.delete_scripts, f"JS error deleting page scripts", e)

    # @print_class_name
    def wait_class_present(self, class_: str) -> None:
        """
        Wait for the given class to be present.

        Args:
            class_ (str): class name to wait
        """
        try:
            # print(f"Waiting presence of elements with class {class_}...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, class_)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_class_present, f"Time exceeded waiting for elements with class {class_}", e)

    # @print_class_name
    def wait_tag_present(self, tag: str) -> None:
        """
        Wait for the given tag to be present.

        Args:
            tag (str): tag name to wait
        """
        try:
            # print(f"Waiting presence of elements with tag {tag}...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, tag)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_tag_present, f"Time exceeded waiting for elements with tag {tag}", e)

    # @print_class_name
    def wait_css_present(self, selector: str) -> None:
        """
        Wait for the presence of element with the given css selector on the page.

        Args:
            selector (str): css selector to wait
        """
        try:
            # print(f"Waiting presence of elements with css selector {selector}...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_css_present, f"Time exceeded waiting for elements with css selector {selector}", e)

    # @print_class_name
    def wait_css_clickable(self, selector: str) -> None:
        """
        Wait for the given css selector to be clickable.

        Args:
            selector (str): css selector to be clickable
        """
        try:
            # print(f"Waiting for css selector {selector} to be clickable...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_css_clickable, f"Time exceeded waiting for elements with css selector {selector} to be clickable", e)

    # @print_class_name
    def wait_css_visible(self, selector: str) -> None:
        """
        Wait for the given css selector to be visible.

        Args:
            selector (str): css selector to be visible
        """
        try:
            # print(f"Waiting for css selector {selector} to be visible...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_css_visible, f"Time exceeded waiting for elements with css selector {selector} to be visible", e)

    # @print_class_name
    def wait_xpath_present(self, xpath: str) -> None:
        """
        Wait for the given xpath to be present.

        Args:
            xpath (str): xpath to wait
        """
        try:
            # print(f"Waiting presence of elements with xpath {xpath}...")
            WebDriverWait(self.__driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException as e:
            BrowserException.print_exception(self.wait_xpath_present, f"Time exceeded waiting for elements with xpath {xpath}", e)

    # @print_class_name
    def find_by_class(self, class_: str, element: WebElement | None = None) -> List[WebElement]:
        """
        Find elements on the current page or given element by class.

        Args:
            class_ (str): elements class
            element (WebElement | None): element to search (only children) if given. None by default
        Returns:
            List[WebElement]; [ ] by default
        """
        try:
            if element:
                # print(f"Finding elements with class {class_} on <{element.tag_name}>...")
                return element.find_elements(By.CLASS_NAME, class_)
            else:
                # print(f"Finding elements with class {class_}...")
                return self.__driver.find_elements(By.CLASS_NAME, class_)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_by_class, f"Elements with class {class_} not found", e)
            return []

    # @print_class_name
    def find_one_by_class(self, class_: str, element: WebElement | None = None) -> WebElement | None:
        """
        Find one element on the current page or given element by class.

        Args:
            class_ (str): element class
            element (WebElement | None): element to search (only children) if given. None by default
        Returns:
            WebElement or None
        """
        try:
            if element:
                # print(f"Finding element with class {class_} on <{element.tag_name}>...")
                return element.find_element(By.CLASS_NAME, class_)
            else:
                # print(f"Finding element with class {class_}...")
                return self.__driver.find_element(By.CLASS_NAME, class_)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_one_by_class, f"Element with class {class_} not found", e)
            return None

    # @print_class_name
    def find_by_tag(self, tag: str, element: WebElement | None = None) -> List[WebElement]:
        """
        Find elements on the current page or given element by tag.

        Args:
            tag (str): elements tag
            element (WebElement | None): element to search (only children) if given. None by default
        Returns:
            List[WebElement]; [ ] by default
        """
        try:
            if element:
                # print(f"Finding elements with tag {tag} on <{element.tag_name}>...")
                return element.find_elements(By.TAG_NAME, tag)
            else:
                # print(f"Finding elements with tag {tag}...")
                return self.__driver.find_elements(By.TAG_NAME, tag)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_by_tag, f"Elements with tag {tag} not found", e)
            return []

    # @print_class_name
    def find_one_by_tag(self, tag: str, element: WebElement | None = None) -> WebElement | None:
        """
        Find one element on the current page or given element by tag.

        Args:
            tag (str): element tag
            element (WebElement | None): element to search (only children) if given. None by default
        Returns:
            WebElement or None
        """
        try:
            if element:
                # print(f"Finding elements with tag {tag} on <{element.tag_name}>...")
                return element.find_element(By.TAG_NAME, tag)
            else:
                # print(f"Finding element with tag {tag}...")
                return self.__driver.find_element(By.TAG_NAME, tag)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_one_by_tag, f"Element with tag {tag} not found", e)
            return None

    # @print_class_name
    def find_by_css(self, selector: str, element: WebElement | None = None) -> List[WebElement]:
        """
        Find elements on the current page or given element by css selector.

        Args:
            selector (str): elements css selector
            element (WebElement | None): element to search if given. None by default
        Returns:
            List[WebElement]; [ ] by default
        """
        try:
            if element:
                # print(f"Finding elements with css selector {selector} on <{element.tag_name}>...")
                return element.find_elements(By.CSS_SELECTOR, selector)
            else:
                # print(f"Finding elements with css selector {selector}...")
                return self.__driver.find_elements(By.CSS_SELECTOR, selector)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_by_css, f"Elements with css selector {selector} not found", e)
            return []

    # @print_class_name
    def find_one_by_css(self, selector: str, element: WebElement | None = None) -> WebElement | None:
        """
        Find one element on the current page or given element by css selector.

        Args:
            selector (str): element css selector. It must include a dot for css classes.
            element (WebElement | None): element to search if given. None by default
        Returns:
            WebElement or None
        """
        try:
            if element:
                # print(f"Finding elements with css selector {selector} on <{element.tag_name}>...")
                return element.find_element(By.CSS_SELECTOR, selector)
            else:
                # print(f"Finding element with css selector {selector}...")
                return self.__driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_one_by_css, f"Element with css selector {selector} not found", e)
            return None

    # @print_class_name
    def find_by_xpath(self, xpath: str, element: WebElement | None = None) -> List[WebElement]:
        """
        Find elements on the current page or given element by xpath.

        Args:
            xpath (str): elements xpath
            element (WebElement | None): element to search if given. None by default
        Returns:
            List[WebElement]; [ ] by default
        """
        try:
            if element:
                # print(f"Finding elements with xpath {xpath} on <{element.tag_name}>...")
                return element.find_elements(By.XPATH, xpath)
            else:
                # print(f"Finding elements with xpath {xpath}...")
                return self.__driver.find_elements(By.XPATH, xpath)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_by_xpath, f"Elements with xpath {xpath} not found", e)
            return []

    # @print_class_name
    def find_one_by_xpath(self, xpath: str, element: WebElement | None = None) -> WebElement | None:
        """
        Find one element on the current page or given element by xpath.

        Args:
            xpath (str): element xpath.
            element (WebElement | None): element to search if given. None by default
        Returns:
            WebElement or None
        """
        try:
            if element:
                # print(f"Finding elements with xpath {xpath} on <{element.tag_name}>...")
                return element.find_element(By.XPATH, xpath)
            else:
                # print(f"Finding element with xpath {xpath}...")
                return self.__driver.find_element(By.XPATH, xpath)
        except NoSuchElementException as e:
            BrowserException.print_exception(self.find_one_by_xpath, f"Element with xpath {xpath} not found", e)
            return None

    @print_class_name
    def quit(self) -> None:
        """
        Close all tabs and quit driver.
        """
        try:
            print("Quitting browser")
            self.__driver.quit()
        except WebDriverException as e:
            BrowserException.print_exception(self.quit, "Browser error on quit", e)


class BrowserException(Exception):
    """Exception raised for browser exceptions.

    Args:
        message (str): exception reason
    """

    def __init__(self, object_, message: str, exception: Exception) -> None:
        self.object_name: Any = object_.__name__
        self.message: str = message
        self.exception: Exception = exception
        super().__init__(BrowserException.__format_exception(object_, message, exception))

    @staticmethod
    def print_exception(object_, message: str, exception: Exception) -> None:
        print(BrowserException.__format_exception(object_, message, exception))

    @staticmethod
    def __format_exception(object_, message: str, exception: Exception) -> str:
        return f"{object_.__name__}: '{message}' | Browser exception: {repr(exception)}"
