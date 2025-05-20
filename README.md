# Code Analysis Script for Artifactory Integration with Agentic AI

This document describes a Python script designed to analyze code baselines stored in Artifactory and provide structured analysis results suitable for consumption by an agentic AI system. The script automates the process of downloading code from Artifactory, extracting it, performing basic analysis (e.g., line counts, pattern searching), and generating a JSON output that an AI agent can easily parse and utilize.

## Purpose

The script aims to:

*   **Automate Code Baseline Retrieval:**  Downloads code artifacts (typically ZIP files) from Artifactory based on specified paths.
*   **Perform Basic Code Analysis:**  Provides initial insights into the code, such as lines of code (using CLOC) and the presence of specific patterns (e.g., "TODO" comments).  This can be extended to include other analysis tools.
*   **Structure Data for AI Agents:**  Generates a JSON output that is easy for AI agents to parse and understand, enabling them to use the analysis results to make decisions and take actions.
*   **Facilitate Code Comparison:** Allows you to analyze two different baselines and compare the results to understand changes and trends in the code.

## Usage

### Prerequisites

*   **Python 3.6+:**  Ensure you have a compatible version of Python installed.
*   **`requests` library:** Install the `requests` library for making HTTP requests:
    ```bash
 pip install requests
    ```
*   **CLOC (Count Lines of Code - Optional):** If you want to use line count analysis, download and install CLOC from [https://github.com/AlDanial/cloc](https://github.com/AlDanial/cloc).  Make sure it's in your system's PATH or set the `CLOC_PATH` variable in the script.
*   **Artifactory Access:** You need valid credentials (username and password or API key) for accessing your Artifactory instance.
*   **Artifactory Artifacts:**  You need to have two code baselines packaged as ZIP files and stored in your Artifactory repository.

### Configuration

Modify the following variables at the beginning of the script to match your environment:

*   `ARTIFACTORY_URL`: The base URL of your Artifactory instance (e.g., `"https://your-artifactory.example.com/artifactory"`).
*   `ARTIFACTORY_USERNAME`: Your Artifactory username.  **Important:**  Consider using environment variables or a secrets management system for storing credentials.
*   `ARTIFACTORY_PASSWORD`: Your Artifactory password or API key. **Important:**  Consider using environment variables or a secrets management system for storing credentials.
*   `BASELINE_1_PATH`: The path to the first code baseline ZIP file in Artifactory (e.g., `"your-repo/baseline1/your-artifact-1.0.0.zip"`).
*   `BASELINE_2_PATH`: The path to the second code baseline ZIP file in Artifactory (e.g., `"your-repo/baseline2/your-artifact-2.0.0.zip"`).
*   `TEMP_DIR`: The temporary directory where the downloaded and extracted code will be stored (default: `"temp_code_analysis"`).
*   `CLOC_PATH`: The path to the CLOC executable (e.g., `"/usr/local/bin/cloc"`).  Update this if CLOC is installed in a different location.

**Example Configuration:**

```python
ARTIFACTORY_URL = "https://my-artifactory.company.com/artifactory"
ARTIFACTORY_USERNAME = "my_user"
ARTIFACTORY_PASSWORD = "my_api_key" # Or your password
BASELINE_1_PATH = "my-repo/project/baseline-1.0.zip"
BASELINE_2_PATH = "my-repo/project/baseline-2.0.zip"
TEMP_DIR = "temp_code_analysis"
CLOC_PATH = "/usr/local/bin/cloc"
