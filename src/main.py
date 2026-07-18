import os
from input.docx_handler import docx_handler
import traceback


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "input", "Red Herring Prospectus.docx")
    output_path = os.path.join(base_dir, "data", "output", "redacted.docx")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Starting PII redaction process")
    print(f"Reading from: {input_path}")
    
    try:
        handler = docx_handler(input_path, output_path)
        handler.process_and_save()
        print("")
        print(f"Success! Redaction of document done and saved!!")
    except FileNotFoundError:
        print("")
        print(f"Error: Could not find the input file at {input_path}")
        print("")
    except Exception as e:
        # print("")
        # print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
