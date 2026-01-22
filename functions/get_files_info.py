import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        result = []
        if directory == ".":
            result.append("Result for current directory:")
        else:
            result.append(f"Result for '{directory}' directory:")

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            result.append(
                f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
            )
            return "\n".join(result)

        if not os.path.isdir(target_dir):
            result.append(f'\tError: "{directory}" is not a directory')
            return "\n".join(result)

        for entry in os.scandir(target_dir):
            file_size = entry.stat().st_size if entry.is_file() else 0
            result.append(
                f"\t- {entry.name}: file_size={file_size} bytes, is_dir={os.path.isdir(entry.path)}"
            )

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
