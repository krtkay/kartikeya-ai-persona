import requests
import base64

from backend.config import GITHUB_TOKEN


class GitHubIngestor:

    def __init__(self, username):

        self.username = username

        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

    def get_repositories(self):

        url = (
            f"https://api.github.com/users/"
            f"{self.username}/repos"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    def get_readme(
        self,
        repo_name
    ):

        url = (
            f"https://api.github.com/repos/"
            f"{self.username}/"
            f"{repo_name}/readme"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        if response.status_code != 200:

            print(
                f"README API Error "
                f"{repo_name}: "
                f"{response.status_code}"
            )

            return None

        data = response.json()

        return base64.b64decode(
            data["content"]
        ).decode(
            "utf-8",
            errors="ignore"
        )

    def get_commits(
        self,
        repo_name,
        limit=20
    ):

        url = (
            f"https://api.github.com/repos/"
            f"{self.username}/"
            f"{repo_name}/commits"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        if response.status_code != 200:

            print(
                f"Commit API Error "
                f"{repo_name}: "
                f"{response.status_code}"
            )

            return []

        commits = response.json()

        return commits[:limit]

    def get_languages(
        self,
        repo_name
    ):

        url = (
            f"https://api.github.com/repos/"
            f"{self.username}/"
            f"{repo_name}/languages"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        if response.status_code != 200:
            return {}

        return response.json()