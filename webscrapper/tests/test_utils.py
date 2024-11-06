import unittest

from webscrapper.utils import Files, print_class_name, os, shutil


class UtilsTest(unittest.TestCase):

    class __Hello:

        @staticmethod
        @print_class_name
        def say_hello() -> None:
            print("Hello")

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        path1: str = Files.create_path_outside("test.txt")
        path2: str = Files.create_path_outside("test2.txt")
        paths: list[str] = [path1, path2]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

        folder_path: str = Files.create_path_outside("files")
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

        return super().tearDown()

    @unittest.skipIf(True, "Success")
    def test_get_project_folder(self) -> None:
        print(Files.get_project_folder())

    @unittest.skipIf(True, "Success")
    def test_get_parent_folder(self) -> None:
        print(Files.get_parent_folder())

    @unittest.skipIf(True, "Success")
    def test_create_path_inside(self) -> None:
        path: str = Files.create_path_inside("test.txt")
        print(path)

    @unittest.skipIf(True, "Success")
    def test_create_path_outside(self) -> None:
        path: str = Files.create_path_outside("test.txt")
        print(path)

    @unittest.skip("Success")
    def test_print_class_name(self) -> None:
        UtilsTest.__Hello.say_hello()

    @unittest.skip("Success")
    def test_create_file(self) -> None:
        Files.create_file("test.txt", "This is a text file")
        path: str = Files.create_path_outside("test.txt")
        self.assertTrue(os.path.exists(path))

    @unittest.skip("Success")
    def test_file_exists(self) -> None:
        Files.create_file("test.txt", "This is a text file")
        path: str = Files.create_path_outside("test.txt")
        self.assertTrue(Files.file_exists(path))

    @unittest.skip("Success")
    def test_copy_file(self) -> None:
        Files.create_file("test.txt", "This is a text file")
        Files.copy_file("test.txt", "test2.txt")
        self.assertTrue(Files.file_exists("test.txt") == Files.file_exists("test2.txt") == True)

    @unittest.skip("Success")
    def test_create_folder(self) -> None:
        Files.create_folder("files")
        self.assertTrue(os.path.isdir(Files.create_path_outside("files")))

    @unittest.skip("Success")
    def test_count_files(self) -> None:
        folder_path: str = Files.create_path_outside("files")
        os.makedirs(folder_path, exist_ok=True)
        Files.create_file("files\\test.txt", "This is a text file")
        Files.create_file("files\\test2.txt", "This is a text file")
        self.assertTrue(Files.count_files("files") == 2)
