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

Output
The script generates a JSON output that contains the analysis results for both code baselines. The JSON structure is as follows:

{
  "baseline1": {
 "artifact_path": "your-repo/baseline1/your-artifact-1.0.0.zip",
 "analysis": {
   "cloc": {
     "header": { ... },
     "SUM": { ... },
     "Bourne Shell": { ... },
     // ... other languages and summaries
   },
   "todo_count": 12
 }
  },
  "baseline2": {
 "artifact_path": "your-repo/baseline2/your-artifact-2.0.0.zip",
 "analysis": {
   "cloc": {
     "header": { ... },
     "SUM": { ... },
     "Bourne Shell": { ... },
     // ... other languages and summaries
   },
   "todo_count": 8
 }
  }
}


artifact_path: The path to the artifact in Artifactory.
analysis: A dictionary containing the analysis results.
cloc: The output from CLOC, if available. Contains line counts for different languages.
todo_count: The number of "TODO" comments found in the code.
Other analysis results can be added here.


Integration with Agentic AI
This script is designed to be used as a tool by an agentic AI system. Here's how it can be integrated:

Agent Task Definition: The AI agent needs to be given a task related to code analysis, such as:

"Analyze the code quality of the latest version of the software."
"Compare the number of TODO comments between two versions of the code."
"Identify potential security vulnerabilities in the codebase."
Tool Selection: The AI agent recognizes that it needs a code analysis tool to accomplish the task and selects this script (or a similar tool).

Configuration: The AI agent populates the configuration variables in the script based on its knowledge or by querying other tools/APIs:

Retrieves Artifactory credentials from a secure secrets management system.
Determines the paths to the code baselines in Artifactory.
Execution: The AI agent executes the script, providing the configuration variables as input.

Result Parsing: The AI agent parses the JSON output generated by the script.

Decision Making: The AI agent uses the analysis results to make decisions and take actions, such as:

Generating a report on the code quality.
Creating a task to address the TODO comments.
Triggering a security scan based on the identified vulnerabilities.
Considerations for Agentic Use
Security: Never hardcode passwords or API keys directly in the script. Use environment variables or a secure secrets management system. The AI agent should be responsible for providing the credentials at runtime.
Resource Limits: Be mindful of the resources (CPU, memory, disk space) that the script consumes. If the codebases are very large, the analysis could take a long time and consume a lot of resources. Consider using techniques like parallel processing or sampling to reduce the resource requirements.
Sandboxing: It's generally a good idea to run the script in a sandboxed environment to prevent it from accessing sensitive resources or making unintended changes to the system. Docker containers are a good option for sandboxing.
Idempotency: Ideally, the script should be idempotent, meaning that it produces the same results if it is run multiple times with the same input. This is important for ensuring that the AI agent can reliably use the script without causing unintended side effects.
API Keys & Authentication: This example uses basic authentication. For production systems, consider using a more secure authentication method, such as API keys or OAuth. The AI agent should be responsible for managing the authentication process.
Dynamic Analysis: The analyze_code function currently performs static analysis. You could extend it to perform dynamic analysis by running the code in a controlled environment and monitoring its behavior. This would require additional tools and infrastructure.
Automated Retries: The AI agent should be able to handle failures and automatically retry the script if necessary. This could involve implementing a retry mechanism in the agent or using a workflow engine that supports automated retries.
Extensibility: Design the analyze_code function to be easily extensible so new analysis tools can be added dynamically. Consider using a plugin architecture or configuration files to allow the AI agent to specify which analysis steps to perform.
