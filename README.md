# DoMyDA

## Project Overview
This project is designed to automate the process of solving data analysis quizzes delivered via web pages. The quizzes require scraping, data processing, and submitting answers via HTTP POST requests. The workflow is as follows:

1. **Receive Quiz URL**: The script receives a quiz URL and a secret (provided via Google Form).
2. **Verify Secret**: The script verifies that the provided secret matches the one you submitted in the Google Form.
3. **Visit Quiz Page**: The script visits the quiz page, which is rendered with JavaScript and contains a data-related task.
4. **Solve Quiz**: The script scrapes the page, processes the data (e.g., sum, filter, analyze, visualize), and determines the correct answer.
5. **Submit Answer**: The script submits the answer to the specified endpoint using a JSON payload:
   ```json
   {
     "email": "your email",
     "secret": "your secret",
     "url": "quiz url",
     "answer": <answer>
   }
   ```
   - Respond with HTTP 200 and JSON if the secret matches.
   - Respond with HTTP 400 for invalid JSON.
   - Respond with HTTP 403 for invalid secrets.
6. **Handle Response**: If the answer is correct, a new quiz URL may be provided. The process repeats until no new URL is given.

## Features
- Headless browser support for JavaScript-rendered pages
- Data scraping and extraction
- Data analysis and transformation
- Automated answer submission
- Error handling for invalid secrets and payloads
- Support for various answer types (number, string, boolean, file, JSON)

## Usage
1. Clone the repository.
2. Install dependencies (see below).
3. Run the script with your email, secret, and quiz URL.

## Example
To test your endpoint, send a POST request to the demo endpoint:
```json
{
  "email": "your email",
  "secret": "your secret",
  "url": "https://tds-llm-analysis.s-anand.net/demo"
}
```

## Dependencies
- Python 3.8+
- [Playwright](https://playwright.dev/python/) or [Selenium](https://www.selenium.dev/) for headless browser automation
- Requests for HTTP requests
- Pandas, NumPy for data analysis

## Running the Script
```bash
python solve_quiz.py --email <your_email> --secret <your_secret> --url <quiz_url>
```

## Error Handling
- HTTP 200: Secret matches, valid answer
- HTTP 400: Invalid JSON payload
- HTTP 403: Invalid secret

## License
MIT
