import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_abs]
        if args:
            command.extend(args)

        proc = subprocess.run(
            command,
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

        output = []

        if proc.returncode != 0:
            output.append(f"Process exited with code {proc.returncode}")

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if stdout:
            output.append(f"STDOUT:\n{stdout}")
        else:
            output.append("STDOUT:")

        if stderr:
            output.append(f"STDERR:\n{stderr}")
        else:
            output.append("STDERR:")

        if not stdout and not stderr:
            output.append("No output produced")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output. Use this when asked to run, execute, or launch a Python script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory (e.g., 'main.py', 'scripts/test.py')",
            ),
            "arguments": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Command line argument to pass to the Python file",
                ),
                description="List of command line arguments to pass to the Python file (optional)",
            ),
        },
        required=["file_path"],  # Tylko file_path jest wymagany
    ),
)
