from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the dataset
file_path = "math_questions_dataset.csv"
data = pd.read_csv(file_path)
data['Options'] = data['Options'].apply(lambda x: eval(x))

# Points for each difficulty level
points = {'Easy': 1, 'Medium': 2, 'Hard': 3}

def get_proficiency_level(prof_score):
    if prof_score >= 75:
        return 'high'
    elif prof_score >= 50:
        return 'medium'
    else:
        return 'low'

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear()
        session['questions'] = data.sample(n=6, random_state=32).to_dict(orient='records')
        session['current_question'] = 0
        session['student_answers'] = []
        session['answer_times'] = []
        session['prof_score'] = 0
        session['total_time_adjusted'] = 0
        session['questions_asked'] = 0
        return redirect(url_for('question'))
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer is None:
            return redirect(url_for('question'))
        start_time = session['start_time']
        end_time = time.time()

        question_data = session['questions'][session['current_question']]
        correct_answer = str(question_data['Answer']).strip().lower()
        student_answer = str(question_data['Options'][int(answer) - 1]).strip().lower()
        difficulty = question_data['Difficulty']
        max_points_for_question = points[difficulty]

        adjusted_time = end_time - start_time
        if difficulty == 'Easy':
            adjusted_time *= 2
        elif difficulty == 'Hard':
            adjusted_time /= 2

        session['total_time_adjusted'] += adjusted_time
        session['student_answers'].append(student_answer)
        session['answer_times'].append((adjusted_time, difficulty))

        if correct_answer == student_answer:
            session['prof_score'] += max_points_for_question

        session['current_question'] += 1
        if session['current_question'] >= len(session['questions']):
            # Calculate initial proficiency
            difficulty_counts = pd.Series([q['Difficulty'] for q in session['questions']]).value_counts().to_dict()
            max_score = sum(points[difficulty] * count for difficulty, count in difficulty_counts.items())
            proficiency = (session['prof_score'] / max_score) * 100

            # Normalize time factor to have an effect of ±10%
            total_time_adjusted = session['total_time_adjusted']
            total_questions = len(session['questions'])
            if total_time_adjusted > 0:
                time_factor = (total_questions / total_time_adjusted) * 10 / 100
            else:
                time_factor = 0  # Avoid division by zero

            time_factor = max(min(time_factor, 0.1), -0.1)  # Limit time factor to ±10%

            initial_proficiency = proficiency * (1 + time_factor)
            initial_proficiency = min(max(initial_proficiency, 0), 100)  # Ensure proficiency stays within 0-100%

            session['initial_proficiency'] = initial_proficiency
            session['question_difficulties'] = [q['Difficulty'] for q in session['questions']]
            session['questions_asked'] = len(session['questions'])
            return redirect(url_for('next_question'))

    if session['current_question'] < len(session['questions']):
        session['start_time'] = time.time()
        question_data = session['questions'][session['current_question']]
        return render_template('question.html', question=question_data, question_number=session['current_question'] + 1, enumerate=enumerate)
    else:
        return redirect(url_for('next_question'))

@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer is None:
            return redirect(url_for('next_question'))
        start_time = session['start_time']
        end_time = time.time()

        question_data = session['next_question_data']
        correct_answer = str(question_data['Answer']).strip().lower()
        student_answer = str(question_data['Options'][int(answer) - 1]).strip().lower()
        difficulty = question_data['Difficulty']
        max_points_for_question = points[difficulty]

        adjusted_time = end_time - start_time
        if difficulty == 'Easy':
            adjusted_time *= 2
        elif difficulty == 'Hard':
            adjusted_time /= 2

        session['total_time_adjusted'] += adjusted_time
        session['student_answers'].append(student_answer)
        session['answer_times'].append((adjusted_time, difficulty))

        if correct_answer == student_answer:
            session['prof_score'] += max_points_for_question

        session['questions_asked'] += 1
        session['question_difficulties'].append(difficulty)

        # Update proficiency
        session['initial_proficiency'] = calculate_adjusted_proficiency(
            session['prof_score'],
            session['question_difficulties'],
            points,
            session['total_time_adjusted'],
            session['questions_asked']
        )
        return redirect(url_for('next_question'))

    proficiency_level = get_proficiency_level(session['initial_proficiency'])

    if proficiency_level == 'high':
        difficulty_choice = ['Hard']
    elif proficiency_level == 'medium':
        difficulty_choice = ['Medium']
    else:
        difficulty_choice = ['Easy']

    next_question = data[data['Difficulty'].isin(difficulty_choice)].sample(n=1, random_state=random.randint(1, 1000)).to_dict(orient='records')[0]

    session['next_question_data'] = next_question
    session['start_time'] = time.time()

    return render_template('next_question.html', question=next_question, question_number=session['questions_asked'] + 1, enumerate=enumerate, proficiency=session['initial_proficiency'])

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        return redirect(url_for('index'))
    
    correct_count = sum([str(q['Answer']).strip().lower() == a for q, a in zip(session['questions'], session['student_answers'])])
    total_questions = len(session['questions'])
    accuracy = correct_count / total_questions
    prof_score = session['prof_score']
    total_time_adjusted = session['total_time_adjusted']
    difficulty_counts = pd.Series([q['Difficulty'] for q in session['questions']]).value_counts().to_dict()
    max_score = sum(points[difficulty] * count for difficulty, count in difficulty_counts.items())
    proficiency = (prof_score / max_score) * 100

    if total_time_adjusted > 0:
        time_factor = (total_questions / total_time_adjusted) * 10 / 100
    else:
        time_factor = 0

    time_factor = max(min(time_factor, 0.1), -0.1)
    initial_proficiency = proficiency * (1 + time_factor)
    initial_proficiency = min(max(initial_proficiency, 0), 100)

    return render_template('results.html', score=correct_count, total=total_questions, accuracy=accuracy * 100, proficiency=initial_proficiency)

if __name__ == '__main__':
    app.run(debug=True)
