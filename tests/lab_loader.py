"""Lesson folders have hyphens in their names, so tests load their scripts by path."""

import importlib.util
from pathlib import Path

LESSONS = Path(__file__).resolve().parents[1] / "lessons"


def load(lesson: str, script: str):
    name = f"{lesson}.{script}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, LESSONS / lesson / f"{script}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
