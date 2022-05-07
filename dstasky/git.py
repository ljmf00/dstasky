from __future__ import annotations

import os

from dstasky.utils import get_data_directory

from typing import Sequence

import pygit2

class ConfigWrapper:
    def __init__(self, config: pygit2.Config) -> None:
        self._config = config

    def __getitem__(self, key: str) -> str | None:
        try:
            return self._config[key]
        except KeyError:
            return None


def get_repo() -> pygit2.Repository:
    data_dir = get_data_directory()
    git_repo_path = pygit2.discover_repository(data_dir)

    return pygit2.Repository(git_repo_path)

def get_author_committer(
        config: pygit2.Config
    )-> tuple[pygit2.Signature | None, pygit2.Signature | None]:
    wconfig = ConfigWrapper(config)
    committer_name = os.environ.get('GIT_COMMITTER_NAME') or \
        wconfig['committer.name'] or \
        wconfig['user.name'] or \
        wconfig['author.name']  # fallback to author lastly

    committer_email = os.environ.get('GIT_COMMITTER_EMAIL') or \
        wconfig['committer.email'] or \
        wconfig['user.email'] or \
        wconfig['author.email']  # fallback to author lastly

    if committer_name and committer_email:
        committer = pygit2.Signature(committer_name, committer_email)
    else:
        committer = None

    author_name = os.environ.get('GIT_AUTHOR_NAME') or \
        wconfig['author.name'] or \
        wconfig['user.name'] or \
        wconfig['commiter.name']  # fallback to commiter lastly

    author_email = os.environ.get('GIT_AUTHOR_EMAIL') or \
        wconfig['author.email'] or \
        wconfig['user.email'] or \
        wconfig['commiter.email']  # fallback to commiter lastly

    if author_name and author_email:
        author = pygit2.Signature(author_name, author_email)
    else:
        author = None

    return author, committer


def is_clean_status(
        repo: pygit2.Repository(),
        files: Sequence[str] = [],
    ) -> bool:
    status = repo.status()
    for filepath, flags in status.items():
        if flags != pygit2.GIT_STATUS_CURRENT and filepath not in files:
            return False

    return True


def ensure_clean_status(
        repo: pygit2.Repository,
        files: Sequence[str] = [],
    ) -> None:
    if not is_clean_status(repo, files):
        raise RuntimeError(
                'Please clean the staged files from the git index before committing!'  # noqa: E501
        )


def create_commit(
        title: str,
        body: str | None,
        *,
        files: Sequence[str],
    ) -> pygit2.Commit:
    repo = get_repo()

    ensure_clean_status(repo, files)

    if repo.is_empty:
        ref = 'HEAD'
        parents = []
    else:
        ref = repo.head.name
        parents = [repo.head.target]

    # write git index
    index = repo.index
    for file in files:
        index.add(file)
    index.write()

    # write git tree
    tree = index.write_tree()

    author, committer = get_author_committer(repo.config)

    message = title
    if body:
        message = message + '\n' + body

    return repo.create_commit(ref, author, committer, message, tree, parents)
