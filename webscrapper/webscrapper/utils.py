import os
import shutil
import time
from functools import wraps
from typing import Any, Generator


def print_class_name(func):
    """
    Print the class name of the class that prints a message in the decorated method

    Args:
        func (str): decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        qualified_name: str = func.__qualname__
        class_name: str = qualified_name.split(".")[0]
        print(f"-> Class {class_name}: ", end="")
        return func(*args, **kwargs)

    return wrapper


class Files:

    __project_folder: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    __parent_folder: str = os.path.dirname(os.path.dirname(__project_folder))

    @staticmethod
    def get_project_folder() -> str:
        return Files.__project_folder

    @staticmethod
    def get_parent_folder() -> str:
        return Files.__parent_folder

    @staticmethod
    def create_path_inside(name: str) -> str:
        """
        Return the absolute path of the given file name related to the project folder.

        Args:
            name (str): file name with extension
        Returns:
            str
        """
        return os.path.join(Files.get_project_folder(), name)

    @staticmethod
    def create_path_outside(name: str) -> str:
        """
        Return the absolute path of the given file name related to project folder parent.

        Args:
            name (str): file name with extension
        Returns:
            str
        """
        return os.path.join(Files.get_parent_folder(), name)

    @staticmethod
    def create_file(path: str, text: str = "") -> None:
        """
        Create a non binary file.

        Args:
            name (str): file name with extension
            text (str): file content
        """
        with open(file=Files.create_path_outside(path), mode="w+", encoding="utf8") as file:
            file.write(text)
            file.close()

    @staticmethod
    def read_file(name: str) -> Generator[str, Any, None]:
        with open(file=Files.create_path_inside(name), mode="r", encoding="utf8") as file:
            for line in file:
                yield line.strip()

    @staticmethod
    def copy_file(origin_file, copied_file: str) -> None:
        """
        Copy the file at origin path on the final path.

        Args:
            origin_file (str): name of of file to be copied
            copied_file (str): path of result file
        """
        shutil.copyfile(Files.create_path_outside(origin_file), Files.create_path_outside(copied_file))

    @staticmethod
    def file_exists(name: str) -> bool:
        """
        Check if the file name exists at package parent folder.

        Args:
            name (str): file name with extension
        Returns:
            bool
        """
        return os.path.exists(Files.create_path_outside(name))

    @staticmethod
    def create_folder(name: str) -> None:
        """
        Create folder at project parent folder.
        """
        os.makedirs(Files.create_path_outside(name), exist_ok=True)

    @staticmethod
    def count_files(folder: str) -> int:
        """
        Count files at outside path.
        """
        return len(os.listdir(Files.create_path_outside(folder)))


class Timer:

    def __init__(self) -> None:
        """
        Start a timer to measure code time.
        """
        self.__start: float
        self.__end: float

    @property
    def start(self) -> float:
        return self.__start

    @property
    def end(self) -> float:
        return self.__end

    def start_timer(self) -> None:
        self.__start = time.time()
        self.__end = self.__start

    def stop_timer(self) -> None:
        self.__end = time.time()

    def get_elapsed_time(self) -> float:
        return self.__end - self.__start
