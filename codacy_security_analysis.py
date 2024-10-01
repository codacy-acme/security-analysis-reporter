import os
import requests
import json
import csv
from typing import List, Dict, Any

class CodacyAPI:
    BASE_URL = "https://app.codacy.com/api/v3"

    def __init__(self):
        self.api_token = os.environ.get("CODACY_API_TOKEN")
        self.git_provider = os.environ.get("GIT_PROVIDER")
        self.organization_name = os.environ.get("CODACY_ORGANIZATION_NAME")

        if not all([self.api_token, self.git_provider, self.organization_name]):
            raise ValueError("Missing required environment variables. Please set CODACY_API_TOKEN, GIT_PROVIDER, and CODACY_ORGANIZATION_NAME.")

        self.headers = {
            "api-token": self.api_token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def list_organization_repositories(self) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/organizations/{self.git_provider}/{self.organization_name}/repositories"
        all_repositories = []
        cursor = None

        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            repositories = data.get("data", [])
            all_repositories.extend(repositories)

            pagination = data.get("pagination", {})
            cursor = pagination.get("cursor")

            if not cursor:
                break

        print(f"Total repositories fetched: {len(all_repositories)}")
        return all_repositories

    def list_repository_pull_requests(self, repo_name: str) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/analysis/organizations/{self.git_provider}/{self.organization_name}/repositories/{repo_name}/pull-requests"
        all_pull_requests = []
        cursor = None

        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            pull_requests = data.get("data", [])
            all_pull_requests.extend(pull_requests)

            pagination = data.get("pagination", {})
            cursor = pagination.get("cursor")

            if not cursor:
                break

        print(f"Total pull requests fetched for {repo_name}: {len(all_pull_requests)}")
        return all_pull_requests

    def search_repository_issues(self, repo_name: str, branch_name: str = None) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/analysis/organizations/{self.git_provider}/{self.organization_name}/repositories/{repo_name}/issues/search"
        all_issues = []
        cursor = None

        body = {
            "categories": ["Security"]  # Filter for security issues only
        }
        if branch_name:
            body["branchName"] = branch_name

        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.post(url, headers=self.headers, params=params, json=body)
            response.raise_for_status()
            data = response.json()

            issues = data.get("data", [])
            all_issues.extend(issues)

            pagination = data.get("pagination", {})
            cursor = pagination.get("cursor")

            if not cursor:
                break

        print(f"Total security issues fetched for {repo_name}: {len(all_issues)}")
        return all_issues

def save_to_csv(data: List[Dict[str, Any]], filename: str):
    if not data:
        print(f"No data to save to {filename}")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    try:
        codacy = CodacyAPI()
        repositories = codacy.list_organization_repositories()

        all_data = []

        for repo in repositories:
            repo_name = repo['name']
            print(f"\nProcessing repository: {repo_name}")

            pull_requests = codacy.list_repository_pull_requests(repo_name)

            for pr in pull_requests:
                pr_info = pr.get('pullRequest', {})
                pr_number = pr_info.get('number')
                pr_title = pr_info.get('title')
                pr_status = pr_info.get('status')

                print(f"Processing PR #{pr_number} - {pr_title} (Status: {pr_status})")

                # Get the security issues for the PR's branch
                branch_name = pr_info.get('branchName')
                issues = codacy.search_repository_issues(repo_name, branch_name)

                for issue in issues:
                    issue_data = {
                        'Repository': repo_name,
                        'PR Number': pr_number,
                        'PR Title': pr_title,
                        'PR Status': pr_status,
                        'Issue ID': issue.get('issueId'),
                        'File Path': issue.get('filePath'),
                        'Line Number': issue.get('lineNumber'),
                        'Message': issue.get('message'),
                        'Pattern ID': issue.get('patternInfo', {}).get('id'),
                        'Category': issue.get('patternInfo', {}).get('category'),
                        'Severity': issue.get('patternInfo', {}).get('severityLevel'),
                        'Tool': issue.get('toolInfo', {}).get('name')
                    }
                    all_data.append(issue_data)

        if all_data:
            csv_filename = "codacy_security_issues.csv"
            save_to_csv(all_data, csv_filename)
            print(f"\nAll security issues have been saved to {csv_filename}")
        else:
            print("No security issues found.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.content}")

if __name__ == "__main__":
    main()
