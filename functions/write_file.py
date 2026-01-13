import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file at a path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the target file path
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Ensure target path is within the working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_path])
            == working_dir_abs
        )

        if not valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # If path points to an existing directory, error
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure parent directories exist
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Write (overwrite) the file
        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
