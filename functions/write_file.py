import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the content to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to Files from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The data to write to the file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Extract the directory path from the full file path
        directory = os.path.dirname(target_file)

        if directory:
            os.makedirs(directory, exist_ok=True)
        
        file = open(target_file, "w")
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"