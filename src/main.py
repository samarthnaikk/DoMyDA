# Main entry point for DoMyDA quiz solver
from helpers.helper_functions import parse_quiz_html

if __name__ == "__main__":
    # Path to the quiz HTML file
    quiz_file = "../recieved_data/quiz_1.html"
    # Compute the answer
    answer = parse_quiz_html(quiz_file)
    print(f"Sum of 'value' column in quiz_1.html: {answer}")
