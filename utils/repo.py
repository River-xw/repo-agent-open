from github import Github
import requests
import os
from typing import Dict, List, Optional, Any
from config import CONFIG


def clone_repo(
    platform: str,
    owner: str,
    repo: str,
    dest: str,
) -> bool:
    """clone a repository from GitHub or Gitee to a local destination.

    Args:
        platform (str): Platform to use ("github" or "gitee").
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        dest (str): The local destination path to clone the repository to.
    Returns:
        bool: True if the repository was cloned, False if it already exists.
    """
    import subprocess

    platform = platform.lower()
    if platform == "github":
        url = f"https://github.com/{owner}/{repo}.git"
    elif platform == "gitee":
        url = f"https://gitee.com/{owner}/{repo}.git"
    else:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")

    # Check if the repo has already been cloned
    if os.path.exists(dest):
        return False

    # Clone the repository
    subprocess.run(["git", "clone", url, dest], check=True)
    return True


def pull_repo(
    platform: str,
    owner: str,
    repo: str,
    dest: str,
) -> bool:
    """Pull the latest changes from a repository on GitHub or Gitee.

    Args:
        platform (str): Platform to use ("github" or "gitee").
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
    Returns:
        bool: True if the pull was successful, False otherwise.
    """
    import subprocess
    import os

    platform = platform.lower()
    if platform not in ["github", "gitee"]:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")

    # Check if the repo has already been cloned
    if not os.path.exists(dest):
        raise FileNotFoundError(
            f"The repository {owner}/{repo} does not exist locally."
        )

    # Pull the latest changes
    subprocess.run(["git", "-C", dest, "pull"], check=True)
    return True


def get_github_repo_info(
    owner: str, repo: str, token: Optional[str] = None
) -> Dict[str, Any]:
    """get repository information from GitHub.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): GitHub personal access token. Defaults to None.

    Returns:
        dict: Repository information.
    """
    g = Github(token) if token else Github()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    return {
        "name": repo_obj.name,
        "full_name": repo_obj.full_name,
        "description": repo_obj.description,
        "language": repo_obj.language,
        "stargazers_count": repo_obj.stargazers_count,
        "forks_count": repo_obj.forks_count,
        "open_issues_count": repo_obj.open_issues_count,
        "created_at": repo_obj.created_at,
        "updated_at": repo_obj.updated_at,
    }


def get_gitee_repo_info(
    owner: str, repo: str, token: Optional[str] = None
) -> Dict[str, Any]:
    """get repository information from Gitee.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): Gitee personal access token. Defaults to None.

    Returns:
        dict: Repository information.
    """
    url = f"https://gitee.com/api/v5/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return {
        "name": data.get("name"),
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "language": data.get("language"),
        "stargazers_count": data.get("stargazers_count"),
        "forks_count": data.get("forks_count"),
        "open_issues_count": data.get("open_issues_count"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }


def get_repo_info(
    owner: str,
    repo: str,
    platform: Optional[str] = "github",
) -> Dict[str, Any]:
    """get repository information from GitHub or Gitee.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        platform (str, optional): Platform to use ("github" or "gitee"). Defaults to "github".

    Returns:
        dict: Repository information.
    """
    platform = platform.lower()
    token = CONFIG.get_token(platform)
    if platform == "github":
        return get_github_repo_info(owner, repo, token)
    elif platform == "gitee":
        return get_gitee_repo_info(owner, repo, token)
    else:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")


def get_github_commits(
    owner: str, repo: str, token: Optional[str] = None, per_page: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """get recent commits from a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): GitHub personal access token. Defaults to None.
        per_page (int, optional): Number of commits to retrieve per page. Defaults to 10.

    Returns:
        list: List of commit information.
    """
    g = Github(token) if token else Github()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    commits = repo_obj.get_commits()[:per_page]
    commit_list = []
    for commit in commits:
        commit_list.append(
            {
                "sha": commit.sha,
                "author": commit.author.login if commit.author else None,
                "message": commit.commit.message,
                "date": commit.commit.author.date,
            }
        )
    return commit_list


def get_gitee_commits(
    owner: str, repo: str, token: Optional[str] = None, per_page: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """get recent commits from a Gitee repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): Gitee personal access token. Defaults to None.
        per_page (int, optional): Number of commits to retrieve per page. Defaults to 10.

    Returns:
        list: List of commit information.
    """
    url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {token}"} if token else {}
    params = {"per_page": per_page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    commit_list = []
    for commit in data:
        commit_list.append(
            {
                "sha": commit.get("sha"),
                "author": (
                    commit.get("author", {}).get("login")
                    if commit.get("author")
                    else None
                ),
                "message": commit.get("commit", {}).get("message"),
                "date": commit.get("commit", {}).get("author", {}).get("date"),
            }
        )
    return commit_list


def get_commits(
    owner: str,
    repo: str,
    per_page: Optional[int] = 10,
    platform: Optional[str] = "github",
) -> List[Dict[str, Any]]:
    """get recent commits from a GitHub or Gitee repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): GitHub personal access token. Defaults to None.
        per_page (int, optional): Number of commits to retrieve per page. Defaults to 10.
        platform (str, optional): Platform to use ("github" or "gitee"). Defaults to "github".

    Returns:
        list: List of commit information.
    """
    platform = platform.lower()
    token = CONFIG.get_token(platform)
    if platform == "github":
        return get_github_commits(owner, repo, token, per_page)
    elif platform == "gitee":
        return get_gitee_commits(owner, repo, token, per_page)
    else:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")


def get_github_commit_files(
    owner: str, repo: str, sha: str, token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """get modified files in a specific commit.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        sha (str): The commit SHA.
        token (str, optional): GitHub personal access token. Defaults to None.

    Returns:
        list: List of modified files in the commit.
    """
    g = Github(token) if token else Github()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    commit = repo_obj.get_commit(sha)
    files = []
    for file in commit.files:
        files.append(
            {
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "patch": file.patch,
            }
        )
    return files


def get_gitee_commit_files(
    owner: str, repo: str, sha: str, token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """get modified files in a specific commit from Gitee.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        sha (str): The commit SHA.
        token (str, optional): Gitee personal access token. Defaults to None.

    Returns:
        list: List of modified files in the commit.
    """
    url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/commits/{sha}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    files = []
    for file in data.get("files", []):
        files.append(
            {
                "filename": file.get("filename"),
                "status": file.get("status"),
                "additions": file.get("additions"),
                "deletions": file.get("deletions"),
                "changes": file.get("changes"),
                "patch": file.get("patch"),
            }
        )
    return files


def get_commit_files(
    owner: str,
    repo: str,
    sha: str,
    platform: Optional[str] = "github",
) -> List[Dict[str, Any]]:
    """get modified files in a specific commit from GitHub or Gitee.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        sha (str): The commit SHA.
        platform (str, optional): Platform to use ("github" or "gitee"). Defaults to "github".

    Returns:
        list: List of modified files in the commit.
    """
    platform = platform.lower()
    token = CONFIG.get_token(platform)
    if platform == "github":
        return get_github_commit_files(owner, repo, sha, token)
    elif platform == "gitee":
        return get_gitee_commit_files(owner, repo, sha, token)
    else:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")


def get_repo_commit_info(
    owner: str,
    repo: str,
    max_num: Optional[int] = 10,
    platform: Optional[str] = "github",
) -> Dict[str, Any]:
    """Get repository information along with recent commits and their modified files.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        max_num (Optional[int], optional): Maximum number of commits to retrieve. Defaults to 10.
        platform (Optional[str], optional): Platform to use ("github" or "gitee"). Defaults to "github".
    Returns:
        Dict[str, Any]: Repository information along with recent commits and their modified files.
    """
    platform = platform.lower()
    repo_info = get_repo_info(owner, repo, platform)
    commits = get_commits(owner, repo, max_num, platform)
    for commit in commits:
        sha = commit["sha"]
        files = get_commit_files(owner, repo, sha, platform)
        commit["files"] = files
    return {
        "repo_info": repo_info,
        "commits_count": len(commits),
        "commits": commits,
    }


if __name__ == "__main__":
    # Example usage
    owner = "squatting-at-home123"
    repo = "back-puppet"
    platform = "gitee"
    commit_info = get_repo_commit_info(owner, repo, platform=platform, max_num=5)
    print("Repository Commit Info:", commit_info)
