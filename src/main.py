# Main entry point for DoMyDA quiz solver
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../helpers')))
from helper_functions import parse_quiz_html

if __name__ == "__main__":
    # Path to the quiz HTML file
    quiz_file = "../recieved_data/quiz_1.html"
    # Compute the answer
    answer = parse_quiz_html(quiz_file)
    print(answer)
