import os
import json
import random

class CaseStudyLoader:
    def __init__(self, folder_path):
        self.data = []
        self.file_names = []  # Store the list of file names without the suffix
        self.load_data(folder_path)

    def load_data(self, folder_path):
        """
        Load all jsonline files from the given folder path and store the data.
        """
        # Iterate through all files in the given directory
        for filename in os.listdir(folder_path):
            if filename.endswith(".jsonl"):
                file_name_without_suffix = filename[:-6]  # Remove the .jsonline suffix
                self.file_names.append(file_name_without_suffix)
                file_path = os.path.join(folder_path, filename)
                # Read the .jsonline file line by line
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        try:
                            # Parse the JSON object in each line and add it to the list
                            record = json.loads(line)
                            record["file_name"] = file_name_without_suffix  # Add the file name to the record
                            self.data.append(record)
                        except json.JSONDecodeError:
                            print(f"Error decoding line in file {filename}")

    def get_random_valid_record(self, llm_parsed_result_true, label_true, file_name=None):
        """
        Return a random record with error field being empty and 
        llm_parsed_result and label satisfying the given conditions.
        
        :param llm_parsed_result_true: True or False, whether llm_parsed_result should be True or False
        :param label_true: True or False, whether label should be True or False
        :param file_name: Optional, specify the file name (without suffix) to filter the records
        """
        valid_records = [
            record for record in self.data
            if not record.get("error")
            and record.get("llm_parsed_result") == llm_parsed_result_true
            and record.get("label") == label_true
            and (file_name is None or record.get("file_name") == file_name)
        ]
        
        if not valid_records:
            return None
        
        # Return a random choice from the filtered records
        return random.choice(valid_records)

    def print_record_human_readable(self, record):
        """
        Print a record in a human-readable format.
        
        :param record: The record to be printed
        """
        if not record:
            print("No valid record found.")
            return
        
        # Print the desired fields in a user-friendly way
        cfg = record.get("cfg", "N/A")
        string = record.get("string", "N/A")
        label = record.get("label", "N/A")
        llm_response = record.get("llm_response", "N/A")
        file_name = record.get("file_name", "N/A")

        print("File Name:")
        print(file_name)
        print("\nCFG:")
        print(cfg)
        print("\nString:")
        print(string)
        print("\nLabel:")
        print(label)
        print("\nLLM Response:")
        print(llm_response)

# Example usage:
# folder_path = "path/to/jsonline/folder"
# loader = CaseStudyLoader(folder_path)
# record = loader.get_random_valid_record(llm_parsed_result_true=True, label_true=False, file_name="specific_file_name")
# loader.print_record_human_readable(record)