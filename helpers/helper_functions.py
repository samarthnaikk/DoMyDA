# Helper functions for DoMyDA quiz solver

def verify_secret(secret: str, expected_secret: str) -> bool:
    """Verify if the provided secret matches the expected secret."""
    return secret == expected_secret

import os
from bs4 import BeautifulSoup

def parse_quiz_html(file_path: str) -> int:
    """
    Parse the quiz HTML file and return the sum of the 'value' column in the table on page 2.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    # Find the table on page 2
    page2 = soup.find('div', {'class': 'page', 'data-page': '2'})
    if not page2:
        raise ValueError('Page 2 not found in HTML.')
    table = page2.find('table', {'id': 'data-table'})
    if not table:
        raise ValueError('Data table not found on page 2.')
    total = 0
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            try:
                total += int(cols[1].text.strip())
            except ValueError:
                continue
    return total
