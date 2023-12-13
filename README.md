# User Guide for GitHub Artifact Downloader Script

## Introduction
This guide describes how to use a Python script to automate the downloading and extraction of artifacts from GitHub Actions runs. The script supports two modes of operation: retrieving the GitHub Actions run URL from the clipboard or directly from the command line as an argument. It is specifically designed for easy viewing of Playwright test results.

## Prerequisites
- **GitHub Token:** A `GITHUB_TOKEN` must be set in your environment variables.
- **Python Installation:** Ensure Python 3 is installed along with the following modules: `requests`, `shutil`, `subprocess`, `os`, `zipfile`, `argparse`, and `tkinter`.
  - On Ubuntu, you may need to install Tkinter separately using: `sudo apt-get install python3-tk`
- **npm Installation:** `npm` should be installed for the live server feature.

## How to Use
1. **Prepare GitHub Actions Run URL:**
   - **Clipboard Method:** Copy the URL of the GitHub Actions run related to Playwright tests to your clipboard. The URL format should be `https://github.com/<owner>/<repo>/actions/runs/<run_id>`. In this method, the script argument is not necessary.
   - **Command Line Argument Method:** Have the GitHub Actions run URL ready to be used as a command line argument.

2. **Run the Script:**
   - **Clipboard Method:** Execute the script in your terminal without any arguments. It will read the URL from your clipboard.
   - **Command Line Argument Method:** Execute the script with the URL as an argument, like so: `python3 script_name.py 'https://github.com/<owner>/<repo>/actions/runs/<run_id>'`

    Example (Clipboard Method):
    ```bash
    $ ./artifact-viewer.py 
    Removed existing artifacts directory: /home/yasu/co/artifact-viewer/artifacts
    Downloaded: /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts/playwright-artifacts.zip
    Extracted: /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts/playwright-artifacts.zip to /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts
    Serving "/home/yasu/co/artifact-viewer/artifacts" at http://127.0.0.1:8080
    Ready for changes
    ```

    Example (Command Line Argument Method):
    ```bash
    $ ./artifact-viewer.py https://github.com/tng-coop/shinano/actions/runs/7197772886
    Removed existing artifacts directory: /home/yasu/co/artifact-viewer/artifacts
    Downloaded: /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts/playwright-artifacts.zip
    Extracted: /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts/playwright-artifacts.zip to /home/yasu/co/artifact-viewer/artifacts/playwright-artifacts
    ```

3. **Automatic Processing:**
   The script performs the following operations:
   - Validates the URL.
   - Fetches artifact details from GitHub.
   - Downloads and extracts artifacts to a specified directory.

4. **View Artifacts Content:**
   Extracted content, such as Playwright test results or other artifacts, will be available in the 'artifacts' directory. The script also launches a live server for convenient viewing of the artifacts.


## Troubleshooting
- **GitHub Token Issue:** Ensure that the `GITHUB_TOKEN` is correctly set in your environment variables.
- **Clipboard Problem:** If using the clipboard method, make sure that the GitHub Actions run URL is correctly copied.
- **Command-Line Argument Issue:** When using the command-line method, ensure that the URL is correctly formatted and passed as an argument.
- **Errors During Execution:** Check the console messages for any errors and confirm that all prerequisites, including npm, are met.

## Notes
- This script is tailored for downloading and viewing Playwright test artifacts from GitHub Actions.
- An active internet connection is required to fetch artifacts from GitHub.

