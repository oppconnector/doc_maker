import re

def output_file_name(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Use regex to find the content between the markers
            match = re.search(r'FILE_NAME\{(.*?)\}END_FILE_NAME', content, re.DOTALL)
            
            if match:
                # Group 1 will contain the content between the markers
                extracted_text = match.group(1)
                return extracted_text.strip()  # Remove leading/trailing whitespace
            else:
                print("No content found between the markers.")
                return None
    
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except IOError:
        print(f"An error occurred while reading the file {file_path}.")
        return None

# Example usage
file_path = 'output_template/template.html'
extracted_text = output_file_name(file_path)

if extracted_text:
    print("Extracted Text:", extracted_text)