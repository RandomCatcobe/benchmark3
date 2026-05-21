"""Shared helpers for command modules."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..artifacts import ArtifactStore


def artifact_path(path: str, artifact_root: Optional[str]) -> Path:
    if artifact_root is None:
        return Path(path)
    return ArtifactStore(artifact_root).resolve_user_path(path)
