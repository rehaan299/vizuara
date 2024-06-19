import random
import pandas as pd

# Load the dataset
file_path = "questions.csv"
data = pd.read_csv(file_path)

# Extract all possible answers
all_answers = data['Answer'].unique().tolist()

# Function to generate multiple choice options
def generate_mcq_options(answer, all_answers, num_options=4):
    options = set()
    options.add(answer)
    while len(options) < num_options:
        option = random.choice(all_answers)
        options.add(option)
    return list(options)

# Add multiple choice options to the dataset
data['Options'] = data['Answer'].apply(lambda x: generate_mcq_options(x, all_answers))

# Ensure options are saved as strings in the CSV
data['Options'] = data['Options'].apply(lambda x: str(x))

# Save the updated dataset
updated_file_path = "math_questions_dataset.csv"
data.to_csv(updated_file_path, index=False)

print(f"Updated dataset saved to {updated_file_path}")
