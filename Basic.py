import requests
import os
import zipfile
import io
import stat
import subprocess  # For basic analysis like cloc or grep
import json

# --- Configuration ---
ARTIFACTORY_URL = "YOUR_ARTIFACTORY_URL"  # e.g., "https://your-artifactory.example.com/artifactory"
ARTIFACTORY_USERNAME = "YOUR_ARTIFACTORY_USERNAME"
ARTIFACTORY_PASSWORD = "YOUR_ARTIFACTORY_PASSWORD"  # Or API Key
BASELINE_1_PATH = "your-repo/baseline1/your-artifact-1.0.0.zip" # Path to the zip in Artifactory
BASELINE_2_PATH = "your-repo/baseline2/your-artifact-2.0.0.zip" # Path to the zip in Artifactory

TEMP_DIR = "temp_code_analysis"  # Temporary directory for extracted code
CLOC_PATH = "/usr/local/bin/cloc"  # Path to the CLOC executable (if used)
# --- Functions ---

def download_from_artifactory(artifact_path, destination_dir):
    """Downloads an artifact from Artifactory.

    Args:
        artifact_path: The path to the artifact in Artifactory.
        destination_dir: The directory to save the downloaded artifact.

    Returns:
        The path to the downloaded file, or None if download failed.
    """
    url = f"{ARTIFACTORY_URL}/{artifact_path}"
    try:
        response = requests.get(url, auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD), stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        filename = os.path.join(destination_dir, os.path.basename(artifact_path))
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filename
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {artifact_path}: {e}")
        return None

def extract_zip(zip_file_path, destination_dir):
    """Extracts a zip file to a destination directory."""
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(destination_dir)
        return True
    except zipfile.BadZipFile as e:
        print(f"Error extracting {zip_file_path}: {e}")
        return False

def analyze_code(code_dir):
    """Performs basic code analysis using CLOC and grep (example).

    Args:
        code_dir: The directory containing the code to analyze.

    Returns:
        A dictionary containing analysis results.
    """
    analysis_results = {}

    # 1. Use CLOC to count lines of code (if CLOC is available)
    if os.path.exists(CLOC_PATH):
        try:
            command = [CLOC_PATH, "--json", code_dir]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            cloc_output = json.loads(result.stdout)
            analysis_results["cloc"] = cloc_output
        except subprocess.CalledProcessError as e:
            print(f"CLOC error: {e}")
            analysis_results["cloc"] = {"error": str(e)}
    else:
        analysis_results["cloc"] = {"warning": "CLOC not found.  Install CLOC for line count analysis."}

    # 2. Example: Search for specific patterns (e.g., "TODO")
    try:
        command = ["grep", "-r", "-i", "TODO", code_dir]
        result = subprocess.run(command, capture_output=True, text=True, check=False)  # check=False allows non-zero exit codes (TODO might not exist)
        analysis_results["todo_count"] = len(result.stdout.splitlines())
    except FileNotFoundError:
        analysis_results["todo_count"] = {"error": "grep not found"}
    except Exception as e:
        analysis_results["todo_count"] = {"error": str(e)}

    # Add more analysis steps here as needed (e.g., security scans, dependency analysis)

    return analysis_results


def main():
    """Main function to download, extract, and analyze code baselines."""

    # 1. Create a temporary directory
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 2. Download and analyze baseline 1
    print(f"Downloading baseline 1 from: {BASELINE_1_PATH}")
    baseline_1_zip = download_from_artifactory(BASELINE_1_PATH, TEMP_DIR)
    if baseline_1_zip:
        baseline_1_dir = os.path.join(TEMP_DIR, "baseline1")
        os.makedirs(baseline_1_dir, exist_ok=True)

        if extract_zip(baseline_1_zip, baseline_1_dir):
            print(f"Analyzing baseline 1 in: {baseline_1_dir}")
            baseline_1_analysis = analyze_code(baseline_1_dir)
        else:
            baseline_1_analysis = {"error": "Extraction failed for baseline 1"}
    else:
        baseline_1_analysis = {"error": "Download failed for baseline 1"}

    # 3. Download and analyze baseline 2
    print(f"Downloading baseline 2 from: {BASELINE_2_PATH}")
    baseline_2_zip = download_from_artifactory(BASELINE_2_PATH, TEMP_DIR)
    if baseline_2_zip:
        baseline_2_dir = os.path.join(TEMP_DIR, "baseline2")
        os.makedirs(baseline_2_dir, exist_ok=True)

        if extract_zip(baseline_2_zip, baseline_2_dir):
            print(f"Analyzing baseline 2 in: {baseline_2_dir}")
            baseline_2_analysis = analyze_code(baseline_2_dir)
        else:
            baseline_2_analysis = {"error": "Extraction failed for baseline 2"}
    else:
        baseline_2_analysis = {"error": "Download failed for baseline 2"}

    # 4. Prepare output for the agentic AI
    output = {
        "baseline1": {
            "artifact_path": BASELINE_1_PATH,
            "analysis": baseline_1_analysis
        },
        "baseline2": {
            "artifact_path": BASELINE_2_PATH,
            "analysis": baseline_2_analysis
        }
    }

    # Convert the output to JSON for easy parsing by the agent
    print(json.dumps(output, indent=4))

    # Optionally, save the output to a file:
    with open("code_analysis_results.json", "w") as f:
        json.dump(output, f, indent=4)

    # Cleanup: Remove the temporary directory and its contents
    # shutil.rmtree(TEMP_DIR) #Remove this comment to delete the temporary directory and all files inside


if __name__ == "__main__":
    main()
