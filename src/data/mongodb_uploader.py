import pymongo
import json
import os
import urllib.parse

# MongoDB connection details
username = "" # Replace with your actual username
password = ""  # Replace with your actual password
encoded_password = urllib.parse.quote(password)  # URL encode the password
cluster = "" # Replace with your actual cluster name
database_name = ""  # Replace with your actual database name
collection_name = "" # Replace with your actual collection name
file_path = ""  # Replace with the actual file path

# Connection URI
uri = f"mongodb+srv://{username}:{encoded_password}@{cluster}/{database_name}?retryWrites=true&w=majority"


# Function to load JSON data from file with UTF-8 encoding
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"Encoding error: {e}")


# Function to validate JSON data
def validate_json(data):
    try:
        if isinstance(data, str):
            json.loads(data)
        elif isinstance(data, dict) or isinstance(data, list):
            json.dumps(data)
        else:
            raise ValueError("Data is not a valid JSON format.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


# Function to connect to MongoDB and insert data
def upload_to_mongodb(uri, database_name, collection_name, data):
    client = pymongo.MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    print(f"Successfully inserted data into MongoDB collection {collection_name}.")


# Main function to load data and upload to MongoDB
def main():
    try:
        # Load JSON data
        data = load_json(file_path)

        # Validate JSON data
        validate_json(data)

        # Upload data to MongoDB
        upload_to_mongodb(uri, database_name, collection_name, data)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()