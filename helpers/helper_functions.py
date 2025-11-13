import re
import string

def extract_likely_questions(file_path: str) -> list:
    """
    Extract likely questions from any HTML file using heuristics and basic NLP.
    - Finds text nodes ending with '?' or containing interrogative words.
    - Ignores navigation, boilerplate, and very short texts.
    Returns a list of question strings.
    """
    from bs4 import BeautifulSoup
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    interrogatives = {'what', 'which', 'who', 'whom', 'whose', 'when', 'where', 'why', 'how', 'describe', 'explain', 'give', 'list', 'select', 'choose'}
    candidates = set()

    # Get all visible text nodes
    for el in soup.find_all(text=True):
        txt = el.strip()
        if not txt or len(txt) < 8:
            continue
        # Remove excessive whitespace and punctuation
        txt_clean = txt.translate(str.maketrans('', '', string.punctuation)).strip()
        words = set(w.lower() for w in txt_clean.split())
        # Filter out JSON/config blobs and technical metadata
        if re.match(r'^[\[{].*[\]}]$', txt) or re.search(r'(docs_flag_initialData|info_params|docs-|true|false|null|\{.*\}|\[.*\])', txt):
            continue
        # Heuristic: ends with '?' or contains interrogative word
        if txt.endswith('?') or interrogatives.intersection(words):
            # Ignore boilerplate (navigation, copyright, etc.)
            if len(txt) > 8 and not re.search(r'(copyright|submit|next|previous|back|home|menu|login|logout)', txt, re.I):
                candidates.add(txt)
        # Also: long sentences with numbers or data requests
        elif len(txt) > 30 and re.search(r'(sum|total|average|mean|count|find|compute|calculate|show|enter|answer)', txt, re.I):
            candidates.add(txt)

    return sorted(candidates)
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


def list_received_files(received_dir: str) -> list:
    """Return a list of file paths in `received_dir` (non-recursive).

    Only returns regular files (no directories).
    """
    received_dir = os.path.abspath(received_dir)
    if not os.path.isdir(received_dir):
        return []
    files = []
    for name in os.listdir(received_dir):
        path = os.path.join(received_dir, name)
        if os.path.isfile(path):
            files.append(path)
    return sorted(files)


def file_contains_text(file_path: str, text: str) -> bool:
    """Return True if `text` appears in the file (case-sensitive)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        return text in data
    except Exception:
        return False


def find_files_matching_url(received_dir: str, url: str, exts=None) -> list:
    """Find files in `received_dir` that likely correspond to the given `url`.

    Matching strategy (best-effort):
    - If `url` is a substring of the file contents, it's a match.
    - If the filename contains a segment of the URL path, it's a match.
    - If `exts` is provided, restrict to those extensions (e.g., ['.html', '.js']).
    Returns a list of file paths.
    """
    if exts is None:
        exts = ['.html', '.htm', '.js', '.json', '.txt']
    url = url or ''
    candidates = []
    for path in list_received_files(received_dir):
        if exts and not any(path.lower().endswith(e) for e in exts):
            continue
        matched = False
        # check content
        if url and file_contains_text(path, url):
            matched = True
        else:
            # check filename tokens
            fname = os.path.basename(path).lower()
            # try last segment of url path
            try:
                seg = url.rstrip('/').split('/')[-1].lower()
            except Exception:
                seg = ''
            if seg and seg in fname:
                matched = True
        if matched:
            candidates.append(path)
    return candidates


def read_file_text(file_path: str) -> str:
    """Return the text contents of a file; returns empty string on failure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


def download_quiz_files(url: str, received_dir: str) -> list:
    """
    Download the HTML file from the given URL and save it in received_dir.
    Returns a list of saved file paths (just the HTML for now).
    """
    import requests
    import re
    import os
    from urllib.parse import urlparse

    if not os.path.isdir(received_dir):
        os.makedirs(received_dir, exist_ok=True)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return []

    # Save HTML file
    # Use last segment of URL path for filename
    parsed = urlparse(url)
    fname = parsed.path.rstrip('/').split('/')[-1] or 'index'
    # Remove query string for filename
    fname = re.sub(r'[^a-zA-Z0-9_.-]', '_', fname)
    html_path = os.path.join(received_dir, f'{fname}.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Optionally: parse for linked JS/CSS and download (not implemented yet)
    # For now, just return the HTML file
    return [html_path]
