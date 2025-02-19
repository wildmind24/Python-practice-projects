import requests
import json
import random
import time

# Fetch questions from Open Trivia Database API
def fetch_questions():
    url = "https://opentdb.com/api.php?amount=30&category=19"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0:
            return data['results']
        else:
            print("Error: Failed to fetch questions. Try again later.")
            return []
    else:
        print("Error: Unable to connect to the trivia API.")
        return []

# Arrange questions in preferred format
def arrange_questions(api_questions):
    questions = []
    for q in api_questions:
        options = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(options)  # Shuffle options
        questions.append({
            "question": q["question"],
            "options": options,
            "answer": q["correct_answer"],
            "difficulty": q["difficulty"]
        })
    return questions

# Display question and options
def display_question(question, index):
    print(f"\nQuestion {index + 1}: {question['question']}")
    for i, option in enumerate(question['options'], 1):
        print(f"{i}. {option}")

# Get the user's answer with a time limit
def get_user_answer(timeout=15, num_options=None):
    start_time = time.time()
    try:
        answer = input(f"You have {timeout} seconds to answer: ")
        if time.time() - start_time > timeout:
            print("\nTime's up!")
            return None
        # Convert answer input to integer and validate the range to fit available number of options
        answer_index = int(answer) - 1
        if num_options is not None and (answer_index < 0 or answer_index >= num_options):
            print("Invalid choice. Answer out of range. Question Skipped")
            return None
    except ValueError:
        print("Invalid input. Question skipped.")
        return None

# To check the user's answer
def check_answer(question, user_answer, score):
    if user_answer is None:
        print("No answer given.")
    elif question['options'][user_answer] == question['answer']:
        print("Correct!")
        score += 10
    else:
        print(f"Wrong! The correct answer was: {question['answer']}")
    return score

# Filter questions by difficulty
def filter_questions_by_difficulty(questions, level):
    return [q for q in questions if q['difficulty'] == level]

# Save high scores to a file
def save_high_score(name, score, file_path="high_scores.txt"):
    with open(file_path, 'a') as file:
        file.write(f"{name}: {score}\n")
    print("Score saved successfully!")

# Main quiz game
def play_quiz():
    print("Welcome to the Trivia Quiz Game!")
    print("Fetching questions...\n")
    api_questions = fetch_questions()
    if not api_questions:
        return

    # Arrange questions
    questions = arrange_questions(api_questions)

    # Choose difficulty
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    questions = filter_questions_by_difficulty(questions, difficulty)
    if not questions:
        print(f"No questions found for difficulty: {difficulty}. Exiting.")
        return

    # Initialize game variables
    score = 0
    total_questions = len(questions)

    # Game loop
    for index, question in enumerate(questions):
        display_question(question, index)
        user_answer = get_user_answer(timeout=15, num_options=len(question['options']))
        score = check_answer(question, user_answer, score)
        print(f"Your current score: {score}\n")

    # Game over
    print("\nQuiz Complete!")
    print(f"Your final score is: {score} out of {total_questions * 10}")

    # Save high scores (optional)
    save_score = input("Do you want to save your score? (yes/no): ").lower()
    if save_score == "yes":
        name = input("Enter your name: ")
        save_high_score(name, score)

# Main entry point
if __name__ == "__main__":
    play_quiz()
    
    
    
    