import pandas as pd
import random
import time

# Load the dataset
file_path = "math_questions_dataset.csv"
data = pd.read_csv(file_path)

# Convert the options back to list
data['Options'] = data['Options'].apply(lambda x: eval(x))

# Points for each difficulty level
points = {'Easy': 1, 'Medium': 2, 'Hard': 3}

# Sample initial set of questions
random_questions = data.sample(n=6, random_state=32)  # Fixed random state for consistent initial questions

print("Please answer the following questions:")
student_answers = []
answer_times = []  # List to store the time taken for each answer along with the difficulty
for i, row in random_questions.iterrows():
    print(f"Q{i + 1} :{row['Question']} ({row['Difficulty']})")
    for j, option in enumerate(row['Options'], start=1):
        print(f"{j}. {option}")
    
    start_time = time.time()  # Record the start time
    while True:
        try:
            answer = int(input("Your choice (1-4): ").strip())
            if 1 <= answer <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
    
    end_time = time.time()  # Record the end time
    
    student_answers.append(row['Options'][answer - 1])
    answer_time = end_time - start_time  # Calculate the time taken
    answer_times.append((answer_time, row['Difficulty']))  # Store time and difficulty

# Evaluate initial answers and calculate proficiency
results = []
prof_score = 0
total_time_adjusted = 0

print("\nResults:")
for i, (index, row) in enumerate(random_questions.iterrows()):
    correct_answer = str(row['Answer']).strip().lower()
    student_answer = str(student_answers[i]).strip().lower()
    difficulty = row['Difficulty']
    max_points_for_question = points[difficulty]

    # Apply multipliers to time taken based on difficulty
    if difficulty == 'Easy':
        adjusted_time = answer_times[i][0] * 2
    elif difficulty == 'Medium':
        adjusted_time = answer_times[i][0] * 1
    elif difficulty == 'Hard':
        adjusted_time = answer_times[i][0] / 2
    
    total_time_adjusted += adjusted_time  # Accumulate adjusted times

    if correct_answer == student_answer:
        results.append(True)
        status = "Correct"
        prof_score += max_points_for_question
    else:
        results.append(False)
        status = "Incorrect"
    
    print(f"Q{i + 1}: {row['Question']}")
    print(f"Your answer: {student_answers[i]}")
    print(f"Correct answer: {row['Answer']}")
    print(f"Result: {status}")
    print(f"Time taken: {adjusted_time:.2f} seconds (Adjusted for difficulty)\n")  # Display the adjusted time

# Display final score
correct_count = sum(results)
total_questions = len(results)
accuracy = correct_count / total_questions
print(f"Your score is {correct_count}/{total_questions}, accuracy is {accuracy * 100}%")

# Calculate initial proficiency factoring in adjusted time
difficulty_counts = random_questions['Difficulty'].value_counts().to_dict()
max_score = sum(points[difficulty] * count for difficulty, count in difficulty_counts.items())
proficiency = (prof_score / max_score) * 100

# Normalize time factor to have an effect of ±10%
if total_time_adjusted > 0:
    time_factor = (total_questions / total_time_adjusted) * 10 / 100
else:
    time_factor = 0  # Avoid division by zero

time_factor = max(min(time_factor, 0.1), -0.1)  # Limit time factor to ±10%

initial_proficiency = proficiency * (1 + time_factor)
initial_proficiency = min(max(initial_proficiency, 0), 100)  # Ensure proficiency stays within 0-100%

print(f"Initial Proficiency: {initial_proficiency}%")

# Function to get proficiency level
def get_proficiency_level(prof_score):
    if prof_score >= 75:
        return 'high'
    elif prof_score >= 50:
        return 'medium'
    else:
        return 'low'

# Function to calculate adjusted proficiency
def calculate_adjusted_proficiency(prof_score, question_difficulties, points, total_time_adjusted, total_questions):
    difficulty_counts = pd.Series(question_difficulties).value_counts().to_dict()
    max_score = sum(points[difficulty] * count for difficulty, count in difficulty_counts.items())
    if max_score > 0:
        proficiency = (prof_score / max_score) * 100
        if total_time_adjusted > 0:
            time_factor = (total_questions / total_time_adjusted) * 10 / 100
        else:
            time_factor = 0  # Avoid division by zero
        
        time_factor = max(min(time_factor, 0.1), -0.1)  # Limit time factor to ±10%
        adjusted_proficiency = proficiency * (1 + time_factor)
        return min(max(adjusted_proficiency, 0), 100)  # Ensure proficiency stays within 0-100%
    else:
        return 0

# Continue asking questions based on proficiency
questions_asked = total_questions
question_difficulties = [row['Difficulty'] for _, row in random_questions.iterrows()]

while True:  # Adjust the condition as needed to stop at the desired number of questions
    proficiency_level = get_proficiency_level(initial_proficiency)
    
    # Select the next question based on the current proficiency level
    if proficiency_level == 'high':
        difficulty_choice = ['Hard']
    elif proficiency_level == 'medium':
        difficulty_choice = ['Medium']
    else:
        difficulty_choice = ['Easy']

    next_question = data[data['Difficulty'].isin(difficulty_choice)].sample(n=1, random_state=random.randint(1, 1000))

    question_text = next_question.iloc[0]['Question']
    correct_answer = str(next_question.iloc[0]['Answer']).strip().lower()
    options = next_question.iloc[0]['Options']
    difficulty = next_question.iloc[0]['Difficulty']
    max_points_for_question = points[difficulty]

    # Ask the question
    print(f"\nQ{questions_asked + 1}: {question_text} ({difficulty})")
    for j, option in enumerate(options, start=1):
        print(f"{j}. {option}")
    
    start_time = time.time()  # Record the start time
    while True:
        try:
            answer = int(input("Your choice (1-4): ").strip())
            if 1 <= answer <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
    end_time = time.time()  # Record the end time

    student_answer = options[answer - 1]
    
    # Evaluate the answer
    if student_answer == correct_answer:
        print("Correct!")
        prof_score += max_points_for_question
    else:
        print(f"Incorrect. The correct answer was: {correct_answer}")

    # Apply multipliers to time taken based on difficulty
    if difficulty == 'Easy':
        adjusted_time = (end_time - start_time) * 2
    elif difficulty == 'Medium':
        adjusted_time = (end_time - start_time) * 1
    elif difficulty == 'Hard':
        adjusted_time = (end_time - start_time) / 2

    total_time_adjusted += adjusted_time  # Accumulate adjusted times
    print(f"Time taken: {adjusted_time:.2f} seconds (Adjusted for difficulty)")

    # Update the question history


    questions_asked += 1
    question_difficulties.append(difficulty)

    # Update proficiency
    initial_proficiency = calculate_adjusted_proficiency(prof_score, question_difficulties, points, total_time_adjusted, questions_asked)
    print(f"Updated Proficiency: {initial_proficiency}%")

    # Break the loop if you have asked the desired number of questions
    if questions_asked >= 15:  # Adjust the condition based on your requirement
        break

# Final proficiency score
print(f"\nFinal Proficiency: {initial_proficiency}%")
