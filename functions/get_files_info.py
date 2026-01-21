import os


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
