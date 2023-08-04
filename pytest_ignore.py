# -*- coding: utf-8 -*-

import os

from pathlib import Path
from sh import git, ErrorReturnCode_1, ErrorReturnCode_128

import pytest

paths = set()


def pytest_ignore_collect(collection_path, config):
    try:
        git("check-ignore", collection_path)
    except ErrorReturnCode_1:
        pass
    except ErrorReturnCode_128:
        if collection_path in paths:
            return True
        else:
            root = Path(config.rootdir)
            while not (root / ".gitignore").exists():
                root = root.parent
            for glob in (root / ".gitignore").read_text().split("\n"):
                glob = glob.strip()
                if glob and not glob.startswith("#"):
                    if glob.startswith("/"):
                        glob = glob.split("/")
                        paths.update(
                            set(
                                (root / glob[0]).rglob(
                                    os.sep.join(glob[1:]) if len(glob) > 1 else "*"
                                )
                            )
                        )
                    else:
                        paths.update(set(root.rglob(glob)))
            if collection_path in paths:
                return True
    else:
        return True
