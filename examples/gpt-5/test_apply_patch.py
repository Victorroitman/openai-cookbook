import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parent / "apply_patch.py"
SPEC = importlib.util.spec_from_file_location("apply_patch", MODULE_PATH)
apply_patch = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader is not None
SPEC.loader.exec_module(apply_patch)


def test_assemble_changes_adds_empty_file_without_error():
    commit = apply_patch.assemble_changes({}, {"empty.txt": ""})

    change = commit.changes["empty.txt"]
    assert change.type == apply_patch.ActionType.ADD
    assert change.new_content == ""


def test_assemble_changes_deletes_empty_file_without_error():
    commit = apply_patch.assemble_changes({"empty.txt": ""}, {})

    change = commit.changes["empty.txt"]
    assert change.type == apply_patch.ActionType.DELETE
    assert change.old_content == ""
