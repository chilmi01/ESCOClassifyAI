import pymongo
import csv
import json
import urllib.parse
from esco_skill_extractor import SkillExtractor # Import the skill extraction function

skill_extractor = SkillExtractor()
skill_extractor.skills_threshold = 0.50

# MongoDB connection details
username = "" # Replace with your actual username
password = ""  # Replace with your actual password
encoded_password = urllib.parse.quote(password)  # URL encode the password
cluster = "" # Replace with your actual cluster name
database_name = ""  # Replace with your actual database name
collection_name = "" # Replace with your actual collection name

uri = f"mongodb+srv://{username}:{encoded_password}@{cluster}/{database_name}?retryWrites=true&w=majority"

# CSV mapping file
csv_mapping_file = "ESCO_Mapping_csv.csv"  
csv_occupation_mapping_file = "ESCO_mapping_occupations.csv"

# JSON output file
output_json_file = "2ndoutput_results.json"

# Connect to MongoDB
client = pymongo.MongoClient(uri)
db = client[database_name]
collection = db[collection_name]

# Load the CSV mapping file
link_to_skill = {}
with open(csv_mapping_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')  # Using ';' as the delimiter
    for row in reader:
        if len(row) > 1:
            link = row[0]  # First column: link
            skill_text = row[1]  # Second column: skill text
            link_to_skill[link] = skill_text

# Load the CSV ocupation mapping file
link_to_occupation = {}
with open(csv_occupation_mapping_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  # Using ',' as the delimiter
    for rows in reader:
        if len(rows) > 1:
            links = rows[1]  # First column: link
            occupation_text = rows[2]  # Second column: skill text
            link_to_occupation[links] = occupation_text

# Process each document in the MongoDB collection
results = []
for document in collection.find():
    title = document.get("Title", "")
    abstract = document.get("Abstract", "")
    combined_text = f"{title} {abstract}".strip()
    ads = [combined_text]


    if ads:
        print(f"Processing document: {document.get('Title', '')}")
        print(f"Text to analyze: {ads}")
        # Extract skills using the skill_extractor.get_skills function
        extracted_skill_links = skill_extractor.get_skills(ads)
        extracted_occupation_links = skill_extractor.get_occupations(ads)  
        print(f"Extracted Skill Links: {extracted_skill_links}")
        print(f"Extracted Occupation Links: {extracted_occupation_links}")   
        # Flatten extracted_links to avoid TypeError
        flat_extracted_skill_links = [item for sublist in extracted_skill_links for item in (sublist if isinstance(sublist, list) else [sublist])]
        flat_extracted_occupation_links = [item for sublist in extracted_occupation_links for item in (sublist if isinstance(sublist, list) else [sublist])]

        # Now use the flattened list for mapping
        found_skills = [link_to_skill[link] for link in flat_extracted_skill_links if link in link_to_skill]
        found_occupation = [link_to_occupation[link] for link in flat_extracted_occupation_links if link in link_to_occupation]
        print(found_skills)
        print(found_occupation)

        # Add the results to the document
        document["FoundSkills"] = found_skills
        document["FoundOccupations"] = found_occupation

        # Append the updated document to the results list
        results.append(document)

# Save the results to a JSON file
with open(output_json_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(results, jsonfile, ensure_ascii=False, indent=4, default=str)

print(f"Processed {len(results)} documents. Results saved to {output_json_file}.")
