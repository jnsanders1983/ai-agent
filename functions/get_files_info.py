import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            contents: list[str] = os.listdir(target_dir)
            dir_summary: str = ""
            for file in contents:
                file_path = os.path.join(target_dir, file)
                is_dir = os.path.isdir(file_path)
                size = os.path.getsize(file_path)
                dir_summary += f"- {file}: file_size={size} bytes, is_dir={is_dir}\n"
            return dir_summary
    except Exception as e:
        return f"Error: {e}"