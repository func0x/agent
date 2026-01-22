import unittest

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_root_dir(self):
        result = get_files_info("calculator", ".")

        self.assertIn("Result for current directory:", result)
        self.assertIn("main.py", result)
        self.assertIn("tests.py", result)
        self.assertIn("pkg", result)
        self.assertIn("is_dir=True", result)
        self.assertIn("is_dir=False", result)

    def test_child_dir(self):
        result = get_files_info("calculator", "pkg")

        self.assertIn("Result for 'pkg' directory:", result)
        self.assertIn("calculator.py", result)
        self.assertIn("render.py", result)

    def test_outside_working_dir(self):
        result = get_files_info("calculator", "/bin")

        self.assertIn("Result for '/bin' directory:", result)
        self.assertIn(
            'Error: Cannot list "/bin" as it is outside the permitted working directory',
            result,
        )

    def test_back_outside_working_dir(self):
        result = get_files_info("calculator", "../")

        self.assertIn("Result for '../' directory:", result)
        self.assertIn(
            'Error: Cannot list "../" as it is outside the permitted working directory',
            result,
        )


if __name__ == "__main__":
    unittest.main(exit=False)

    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
