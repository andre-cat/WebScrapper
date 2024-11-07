from dataclasses import dataclass
from typing import Any, List, cast

from bs4 import BeautifulSoup, ResultSet, Tag


@dataclass
class Content:

    text: str
    images: str
    videos: str
    links: str

    def __str__(self):
        return f"{self.text}\n{self.images}\n{self.videos}\n{self.links}"


class Scrapper:

    def __init__(self, source_code: str = "") -> None:
        """
        Create a soup to be scrapped with source code.

        Args:
            source_code (str): html source code to scrap
        """
        if source_code:
            self.set_source_code(source_code)
        else:
            self.__soup: BeautifulSoup = BeautifulSoup("", "html.parser")

    def set_source_code(self, source: str) -> None:
        """
        Set a new soup to be scrapped.

        Args:
            source (str): new source code
        """
        if not source.strip().startswith("<?xml"):
            self.__soup = BeautifulSoup(source, "html.parser")
        else:
            print("This source is not from an HTML page")

    def has_source_code(self) -> bool:
        """
        Check if source code is empty.

        Returns:
            bool
        """
        return bool(self.__soup.contents)

    def print_source_code(self) -> None:
        """
        Print soup source code beautifully.
        """
        print(self.__soup.prettify())

    def set_root(self, tag: Tag) -> None:
        """
        Set the source code of tag as the soup.
        """
        self.set_source_code(str(tag))

    def delete_tags(self, tags: List[str] | str) -> None:
        """
        Delete given tags from soup.

        Args:
            tags (List[str] | str): tags to delete
        """
        if isinstance(tags, str):
            tags = [tags]

        for tag in tags:
            for element in self.__soup.find_all(tag):
                if isinstance(element, Tag):
                    cast(Tag, element).decompose()

    # @print_class_name
    def find_all(self, tags: List[str] | str, classes: List[str] | str | None = None, element: Tag | None = None, recursive: bool = True) -> ResultSet[Tag]:
        """
        Find elements on source code or element.

        Args:
            tags (List[str] | str): elements tags
            classes (List[str] | str | None): elements classes. None by default
            element (Tag | None): element to search if given. None by default
            recursive (bool): recursive search. True by default
        Returns:
            List[Tag]
        """
        # print("Finding elements " + str(tags) + (f" with classes {classes}" if classes else "") + (f" on {element.name}" if element else ""))

        kwargs: dict[str, Any] = {}

        if classes:
            if isinstance(classes, str):
                classes = [classes]
            kwargs["class_"] = " ".join(classes)

        if element:
            return element.find_all(tags, recursive=recursive, **kwargs)
        else:
            return self.__soup.find_all(tags, recursive=recursive, **kwargs)

    # @print_class_name
    def find_one(self, tag: str, classes: List[str] | str | None = None, element: Tag | None = None, recursive: bool = True) -> Tag | None:
        """
        Find one element on source code or element.

        Args:
            tag (str): elements tag
            classes (List[str] | str | None): elements classes. None by default
            element (Tag | None): element to search if given. None by default
            recursive (bool): recursive search. True by default
        Returns:
            Tag | None
        """
        # print("Finding element " + tag + (f" with classes {classes}" if classes else "") + (f" on {element.name}" if element else ""))

        kwargs: dict[str, Any] = {}

        if classes:
            if isinstance(classes, str):
                classes = [classes]
            kwargs["class_"] = " ".join(classes)

        if element:
            return cast(Tag, element.find(tag, recursive=recursive, **kwargs))
        else:
            return cast(Tag, self.__soup.find(tag, recursive=recursive, **kwargs))

    def get_content(self, tag: Tag) -> Content:
        """
        Create a text representation of a tag content.

        Args:
            tag (str): elements tag
        Returns:
            Tag | None
        """

        # This method requires to be optimized

        text: str = ""
        images: str = ""
        videos: str = ""
        links: str = ""

        text += "TEXT\n"
        text += tag.get_text(separator=" ", strip=True)
        text = text.strip()
        text = " ".join(text.split())

        # Adding images
        images_element: ResultSet[Any] = tag.find_all("img", src=True, recursive=True)
        if len(images_element) > 0:
            images += f"IMAGES"
            for image in images_element:
                images += f"\nImage: {image["src"]}"

        # Adding videos
        videos_element: ResultSet[Any] = tag.find_all("video", src=True, recursive=True)
        if len(videos_element) > 0:
            videos += f"VIDEOS"
            for video in videos_element:
                videos += f"\nVideo: {video["src"]}"

        # Adding links
        links_element: ResultSet[Any] = tag.find_all("a", href=True, recursive=True)
        if len(links_element) > 0:
            links += f"LINKS"
            for link in links_element:
                links += f"\nLink: {link["href"]}"

        return Content(text, images, videos, links)
