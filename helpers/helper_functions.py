# Helper functions for DoMyDA quiz solver

def verify_secret(secret: str, expected_secret: str) -> bool:
    """Verify if the provided secret matches the expected secret."""
    return secret == expected_secret

import os
from bs4 import BeautifulSoup

def parse_quiz_html(file_path: str) -> str:
    """
    General parser for quiz HTML files. Extracts questions and answers in a readable format.
    Handles static and dynamically rendered content (e.g., in <div id='result'>).
    """
    import base64
    import re
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract questions from headings
    questions = []
    for tag in ['h1', 'h2', 'h3']:
        for q in soup.find_all(tag):
            questions.append(q.get_text(strip=True))

    # Try to extract question/answer from <div id='result'> (may be rendered via JS)
    result_div = soup.find('div', id='result')
    if result_div:
        # Look for atob in script
        scripts = soup.find_all('script')
        for script in scripts:
            m = re.search(r"atob\(`([A-Za-z0-9+/=\n]+)`\)", script.text)
            if m:
                b64 = m.group(1).replace('\n', '')
                try:
                    decoded = base64.b64decode(b64).decode('utf-8')
                    # Try to extract question and answer from decoded text
                    # If JSON, pretty print
                    if decoded.strip().startswith('{'):
                        import json
                        try:
                            obj = json.loads(decoded)
                            questions.append(f"Decoded JSON: {json.dumps(obj, indent=2)}")
                        except Exception:
                            questions.append(f"Decoded: {decoded}")
                    else:
                        questions.append(f"Decoded: {decoded}")
                except Exception:
                    questions.append("Could not decode base64 content.")

    if not questions:
        questions.append("Question not found.")

    # Format output
    output = ""
    for i, q in enumerate(questions):
        output += f"Question/Info {i+1}: {q}\n"
    return output.strip()
