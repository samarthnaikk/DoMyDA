# Main entry point for DoMyDA quiz solver
import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../helpers')))
from helper_functions import (
    parse_quiz_html,
    list_received_files,
    find_files_matching_url,
    download_quiz_files,
)


def main():
    p = argparse.ArgumentParser(description='DoMyDA quiz processor')
    p.add_argument('--url', '-u', help='The quiz URL or identifier to match files', required=False)
    p.add_argument('--dir', '-d', help='Path to recieved_data directory', default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recieved_data')))
    args = p.parse_args()

    received_dir = args.dir
    url = args.url

    print(f"Scanning received directory: {received_dir}")
    files = list_received_files(received_dir)
    if not files:
        print("No files found in recieved_data.")
        return

    if url:
        matches = find_files_matching_url(received_dir, url)
        if not matches:
            print(f"No files matched the URL: {url}")
            print("Attempting to download from URL...")
            downloaded = download_quiz_files(url, received_dir)
            if not downloaded:
                print("Download failed or no files saved.")
                return
            matches = downloaded
    else:
        # If no url provided, process all html/js/json/text files
        matches = [f for f in files if os.path.splitext(f)[1].lower() in ('.html', '.htm', '.js', '.json', '.txt')]

    # Process each matched file
    for path in matches:
        print('\n' + '='*60)
        print(f"Processing file: {path}")
        try:
            out = parse_quiz_html(path)
            print(out)
        except Exception as e:
            print(f"Error processing {path}: {e}")


if __name__ == '__main__':
    main()
