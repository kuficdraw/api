import json
import os
from datetime import datetime


def formatted_time():
    # Get the current datetime
    current_datetime = datetime.now()
    # Convert the datetime to a string
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_string

def get_filenames_in_directory(directory):
    filenames = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Get all files and directories in the given directory
        items = os.listdir(directory)
        # Iterate through each item
        for item in items:
            # Check if the item is a file
            if os.path.isfile(os.path.join(directory, item)):
                filenames.append(item)
    return filenames

if __name__ == "__main__":
    artworks_directory = "../artworks"

    time = formatted_time()
    files = get_filenames_in_directory(artworks_directory)
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