# Codacy Security Analysis Script

This Python script interacts with the Codacy API to fetch and analyze security issues across all repositories and pull requests in a specified organization. It provides a comprehensive overview of security-related issues detected by Codacy.

## Features

- Fetches all repositories in the specified organization
- Retrieves all pull requests (both open and closed) for each repository
- Collects security issues for each pull request
- Outputs all security issues to a CSV file for easy analysis

## Prerequisites

- Python 3.6 or higher
- `requests` library
- Codacy API token
- Git provider (GitHub, Bitbucket, or GitLab) account connected to Codacy
- Codacy organization name

## Setup

1. Clone this repository or download the script file.

2. Install the required Python library:
   ```
   pip install requests
   ```

3. Set up the following environment variables:
   ```
   export CODACY_API_TOKEN="your_api_token_here"
   export GIT_PROVIDER="your_git_provider_here"
   export CODACY_ORGANIZATION_NAME="your_organization_name_here"
   ```
   
   Note: For `GIT_PROVIDER`, use "gh" for GitHub, "bb" for Bitbucket, or "gl" for GitLab.

## Usage

1. Navigate to the directory containing the script.

2. Run the script:
   ```
   python codacy_security_analysis.py
   ```

3. The script will process all repositories and pull requests, collecting security issues.

4. Once complete, you'll find a CSV file named `codacy_security_issues.csv` in the same directory as the script.

## Output

The `codacy_security_issues.csv` file contains the following information for each security issue:

- Repository name
- Pull Request number
- Pull Request title
- Pull Request status
- Issue ID
- File path
- Line number
- Issue message
- Pattern ID
- Category
- Severity
- Tool name

## Notes

- The script may take a considerable amount of time to run, especially for organizations with many repositories or pull requests.
- Ensure you have the necessary permissions in Codacy to access all repositories and pull requests.
- The script uses pagination to fetch all results, so it should work with large amounts of data.
- If you encounter any errors, check the console output for error messages related to authentication or API access.

## Customization

You can modify the script to change the data being collected or how it's processed. The main logic is in the `main()` function. If you want to change the name of the output file, you can modify the `csv_filename` variable in the `main()` function.

## Security

Keep your Codacy API token secure and never share it publicly. If you're using version control, make sure not to commit the script with your API token hardcoded – always use environment variables for sensitive information.
