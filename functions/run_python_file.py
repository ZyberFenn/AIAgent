import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located in the working directory, optionally with arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        # Absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target file path
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Ensure target path is within working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_path])
            == working_dir_abs
        )

        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Ensure file exists and is a regular file
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Ensure file is a Python file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", target_path]

        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(
                f"Process exited with code {result.returncode}"
            )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr:
            output_parts.append("No output produced")
        else:
            if stdout:
                output_parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                output_parts.append(f"STDERR:\n{stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
