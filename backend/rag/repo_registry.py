from backend.rag.github_ingestor import GitHubIngestor


class RepoRegistry:

    def __init__(self):

        github = GitHubIngestor("krtkay")

        repos = github.get_repositories()

        self.repo_names = [
            repo["name"]
            for repo in repos
        ]

    def get_repo_names(self):

        return self.repo_names