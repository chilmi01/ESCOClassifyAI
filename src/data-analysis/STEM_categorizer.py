import ollama
import pandas as pd

# Define the classification categories
categories = {
    "Science": "Physics, Chemistry, Biology, Environmental Science",
    "Technology": "Computer Science, AI, Software Engineering, IT",
    "Engineering": "Mechanical, Electrical, Civil, Robotics",
    "Mathematics": "Pure Mathematics, Statistics, Data Science"
}

# Function to classify a thesis title + abstract
def classify_thesis(title, abstract):
    prompt = f"""
    You are an AI that classifies university theses into four categories: Science, Technology, Engineering, or Mathematics (STEM).
    Based on the following thesis title and abstract, classify it into the most appropriate category.

    Categories:
    - Science: {categories["Science"]}
    - Technology: {categories["Technology"]}
    - Engineering: {categories["Engineering"]}
    - Mathematics: {categories["Mathematics"]}

    Respond with only one category name.

    Title: {title}
    Abstract: {abstract}

    Category:
    """

    response = ollama.chat(model='deepseek-r1:7b', messages=[{"role": "user", "content": prompt}])

    return response['message']['content'].strip()

# Load data from CSV file (Assuming columns: 'Title', 'Abstract')
input_csv = "thesis_data.csv"  # Change to your CSV file name
df = pd.read_csv(input_csv)

# Apply classification
df['STEM_Category'] = df.apply(lambda row: classify_thesis(row['Title'], row['Abstract']), axis=1)

# Save results to a new CSV file
output_csv = "classified_theses.csv"
df.to_csv(output_csv, index=False)

print(f"Classification complete! Results saved to '{output_csv}'.")
