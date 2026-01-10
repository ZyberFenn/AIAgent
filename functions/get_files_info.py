import os


def get_files_info(working_directory, directory="."):
    try:
        # Get absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct and normalize the target directory path
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Ensure target directory is within the working directory
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir])
            == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure target_dir is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)

            entries.append(
                f"- {item}: file_size={size} bytes, is_dir={is_dir}"
            )

        return "\n".join(entries)

    except Exception as e:
        return f"Error: {e}"
