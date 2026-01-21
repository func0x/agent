import unittest

from config import MAX_CHARS
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def test_truncation_message_added(self):
        result = get_file_content("calculator", "lorem.txt")
        print("!!!!result:", result)

        self.assertGreater(len(result), MAX_CHARS)
        self.assertTrue(
            result.endswith(
                f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
            )
        )

    def test_no_truncation_when_short(self):
        result = get_file_content("calculator", "short.txt")

        self.assertLessEqual(len(result), MAX_CHARS)
        self.assertNotIn("truncated at", result)


if __name__ == "__main__":
    unittest.main(exit=False)

    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
