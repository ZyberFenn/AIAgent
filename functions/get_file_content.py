import os
from config import MAX_FILE_CHARS


def get_file_content(working_directory, file_path):
    try:
        # Absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target file path
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Ensure target file is within working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_path])
            == working_dir_abs
        )

        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure target path is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_FILE_CHARS characters
        with open(target_path, "r") as f:
            content = f.read(MAX_FILE_CHARS)

            # Check if file was truncated
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
