import unittest

from functions.get_file_content import get_file_content
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def test_write_file(self):
        content = "wait, this isn't lorem ipsum"
        write_file("calculator", "test.txt", content)
        result = get_file_content("calculator", "test.txt")
        self.assertLessEqual(len(result), len(content))


if __name__ == "__main__":
    unittest.main(exit=False)

    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
