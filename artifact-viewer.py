#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import requests
import os
import zipfile
import tkinter

def print_help():
    """Prints usage instructions and help information."""
    print("GitHub Artifact Downloader Script")
    print("Usage: Run the script after copying a valid GitHub Actions run URL to your clipboard.")
    print("The URL should be in the format: 'https://github.com/<owner>/<repo>/actions/runs/<run_id>'")

def validate_github_run_url(url):
    """Validate the GitHub Actions run URL and extract repository information."""
    github_run_url_pattern = r'^https://github\.com/([\w-]+)/([\w-]+)/actions/runs/(\d+)'
    match = re.match(github_run_url_pattern, url)
    if match:
        owner, repo, run_id = match.groups()
        return owner, repo, run_id
    else:
        raise ValueError("URL is not a valid GitHub Actions run URL. "
                         "The URL should be in the format: 'https://github.com/<owner>/<repo>/actions/runs/<run_id>'")

# Function to get and validate the clipboard content as a GitHub Actions run URL
def get_clipboard_content():
    try:
        root = tkinter.Tk()
        root.withdraw()
        clipboard_content = root.clipboard_get()
        root.destroy()
    except Exception as e:
        raise RuntimeError(f"Failed to get content from clipboard: {e}")


    # Regular expression to validate GitHub Actions run URL
    github_run_url_pattern = r'^https://github\.com/[\w-]+/[\w-]+/actions/runs/\d+'

    match = re.match(github_run_url_pattern, clipboard_content)
    if match:
        return match.group(0)
    else:
        raise ValueError("Clipboard content is not a valid GitHub Actions run URL. "
                         "The URL should be in the format: 'https://github.com/<owner>/<repo>/actions/runs/<run_id>'")


def extract_artifact(file_path, artifact_subfolder):
    """Extract a zip file to a directory within the artifact subfolder."""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(artifact_subfolder)
    print(f'Extracted: {file_path} to {artifact_subfolder}')

def download_and_extract_artifact(artifact, script_dir, headers):
    """Download and extract a single artifact."""
    response = requests.get(artifact['archive_download_url'], headers=headers, stream=True)
    if response.status_code == 200:
        artifact_name = artifact['name']
        # Create the artifact subfolder path relative to the script's directory
        artifact_subfolder = os.path.join(script_dir, 'artifacts', artifact_name)
        os.makedirs(artifact_subfolder, exist_ok=True)

        filename = artifact_name + '.zip'
        filepath = os.path.join(artifact_subfolder, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded: {filepath}')

        extract_artifact(filepath, artifact_subfolder)
    else:
        print(f'Error downloading {artifact["name"]}: {response.status_code}')

def get_url_from_args():
    """Get GitHub Actions run URL from command line arguments."""
    parser = argparse.ArgumentParser(description="GitHub Artifact Downloader Script")
    parser.add_argument('url', nargs='?', help="GitHub Actions run URL")
    args = parser.parse_args()
    return args.url

def main():
    try:
        # Retrieve the GitHub Token from the environment variable
        token = os.getenv('GITHUB_TOKEN')

        # Ensure that the token is available
        if not token:
            print_help()
            print("GitHub token not found in environment variables. Please set GITHUB_TOKEN.")
            exit(1)

        # Get URL either from arguments or clipboard
        url = get_url_from_args()
        if url is None:
            url = get_clipboard_content()

        owner, repo, run_id = validate_github_run_url(url)

        # GitHub API URL for artifacts of a specific run
        api_url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts'
        # ... [rest of the main function]
        # if any error, print_help and exit
    except Exception as e:
        print_help()
        exit(1)

    # Headers for authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    # Get the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Get the list of artifacts
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f'Error fetching artifacts: {response.status_code}')
        return

    artifacts = response.json()['artifacts']
    if not artifacts:
        print('No artifacts found for this run')
        return

    # Path to the artifacts directory
    artifacts_dir = os.path.join(script_dir, 'artifacts')

    # Check if the artifacts directory exists and remove it
    if os.path.exists(artifacts_dir):
        shutil.rmtree(artifacts_dir)
        print(f'Removed existing artifacts directory: {artifacts_dir}')

    # Download and extract each artifact
    for artifact in artifacts:
        download_and_extract_artifact(artifact, script_dir, headers)

    # Start live server in the 'artifacts' directory
    subprocess.run(['npx', 'live-server', os.path.join(script_dir, 'artifacts')])

if __name__ == '__main__':
    main()
