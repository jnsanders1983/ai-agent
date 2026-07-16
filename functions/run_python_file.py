import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        root, extension = os.path.splitext(absolute_file_path)

        if extension != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)
        
        # Execute the process with the requested configurations
        result = subprocess.run(
            command,
            cwd=working_dir_abs,       # Sets the working directory properly
            capture_output=True,       # Captures stdout and stderr
            text=True,                 # Decodes output to strings instead of bytes
            timeout=30                 # Prevents infinite execution
        )
        
        # Return stdout if successful, or stderr if the script failed
        #if result.returncode == 0:
        #    return result.stdout
        #else:
        #    return f"Script Error (Exit Code {result.returncode}):\n{result.stderr}"
        
        # Building the custom output string
        output_parts = []
        
        # 1. Check for non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        # 2. Check if both stdout and stderr are empty
        # Note: subprocess.run with text=True defaults empty streams to an empty string ("")
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            # 3. Include STDOUT if it contains text
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            
            # 4. Include STDERR if it contains text
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
                
        # Join all the collected parts with newlines
        return "\n".join(output_parts)
    
    except subprocess.TimeoutExpired:
        return "Error: The script execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"