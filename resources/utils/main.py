import json
import os
from datetime import datetime


def convert_timestamp_to_datetime(timestamp):
    # Convert milliseconds to seconds
    timestamp_seconds = timestamp / 1000.0
    # Convert timestamp to datetime object
    return datetime.fromtimestamp(timestamp_seconds)
    
def formatted_time():
    # Get the current datetime
    current_datetime = datetime.now()
    # Convert the datetime to a string
    return format_time(current_datetime)

def format_time(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def get_filenames_sorted_by_modified_time(directory):
    results = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Get all files and directories in the given directory
        items = os.listdir(directory)
        # Iterate through each item
        for item in items:
            # Check if the item is a file
            if os.path.isfile(os.path.join(directory, item)):
                if item != "meta.json":
                    # Get the modification timestamp of the file
                    modified_time = os.path.getmtime(os.path.join(directory, item))
                    # Append filename and modification timestamp to results
                    results.append({"filename": item, "modified_time": modified_time})
    # Sort results by modification time in descending order (most recent first)
    results.sort(key=lambda x: x["modified_time"], reverse=True)
    # Extract and return only the filenames from sorted results
    return [file_info["filename"] for file_info in results]

def get_filenames_sorted_by_created_at_in_json(directory):
    results = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Get all files and directories in the given directory
        items = os.listdir(directory)
        # Iterate through each item
        for item in items:
            # Check if the item is a file
            if os.path.isfile(os.path.join(directory, item)):
                if item != "meta.json":
                    # Read JSON file content to extract createdAt
                    with open(os.path.join(directory, item), 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        try:
                            file_json = json.loads(file_content)
                            created_at = file_json["info"]["createdAt"]
                            results.append({"filename": item, "createdAt": created_at})
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error processing file {item}: {e}")
    # Sort results by createdAt datetime in descending order (most recent first)
    results.sort(key=lambda x: convert_timestamp_to_datetime(x["createdAt"]), reverse=True)
    # Extract and return only the filenames from sorted results
    return [file_info["filename"] for file_info in results]

if __name__ == "__main__":
    artworks_directory = "../artworks"

    time = formatted_time()
    files = get_filenames_sorted_by_created_at_in_json(artworks_directory)
    print(files);

    # Generate the meta dictionary
    meta_data = {
        "last_update": time,
        "files": files
    }
    print(meta_data);

    # Write the meta dictionary to a JSON file
    with open(os.path.join(artworks_directory, 'meta.json'), 'w') as json_file:
        json.dump(meta_data, json_file, indent=2)