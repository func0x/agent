import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = target_file_abs = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        if os.path.commonpath([working_dir_abs, target_file_abs]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_abs, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(get_file_content("calculator", "lorem.txt"))
