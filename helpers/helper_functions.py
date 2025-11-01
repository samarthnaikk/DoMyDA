# Helper functions for DoMyDA quiz solver

def verify_secret(secret: str, expected_secret: str) -> bool:
    """Verify if the provided secret matches the expected secret."""
    return secret == expected_secret

import os
from bs4 import BeautifulSoup

def parse_quiz_html(file_path: str) -> str:
    """
    General parser for quiz HTML files. Extracts all questions and answers in a readable format.
    - Finds questions in <h2>, <h3>, <h1>, and <div id='question'>
    - For each table, lists its headers and rows
    - For tables with a 'value' column, computes the sum
    - Returns a formatted string with all found questions and answers
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract all questions
    questions = []
    for tag in ['h1', 'h2', 'h3']:
        for q in soup.find_all(tag):
            questions.append(q.get_text(strip=True))
    qdiv = soup.find('div', id='question')
    if qdiv:
        questions.append(qdiv.get_text(strip=True))
    if not questions:
        questions.append("Question not found.")

    # Extract all tables and try to find answers
    answers = []
    for table in soup.find_all('table'):
        # Get headers
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        # Get all rows
        rows = []
        for tr in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cols:
                rows.append(cols)
        # If 'value' column exists, compute sum
        if 'value' in headers:
            idx = headers.index('value')
            total = 0
            for row in rows:
                try:
                    total += int(row[idx])
                except (ValueError, IndexError):
                    continue
            answers.append(f"Sum of 'value' column: {total}")
        else:
            # Otherwise, just show table data
            answers.append(f"Table with headers {headers}: {rows}")
    if not answers:
        answers.append("No tables or answers found.")

    # Format output
    output = ""
    for i, q in enumerate(questions):
        output += f"Question {i+1}: {q}\n"
    for i, a in enumerate(answers):
        output += f"Answer {i+1}: {a}\n"
    return output.strip()
