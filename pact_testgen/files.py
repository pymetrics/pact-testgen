import json
from ast import parse
from _ast import Module, FunctionDef
from io import StringIO

from typing import Generator, List
from pathlib import Path
from enum import Enum, auto

try:
    from ast import unparse
except ImportError:
    unparse = None

from pact_testgen.models import Pact


class ProviderStateFileOutcome(Enum):
    WROTE_NEW = auto()
    MERGED = auto()
    LEFT_EXISTING = auto()


def load_pact_file(path: str) -> Pact:
    """Loads the file at the supplied path into a Pact model"""
    with open(Path(path), "r") as f:
        pact = json.load(f)
        return Pact(**pact)


def write_test_file(testfile: str, path: Path):
    with open(path, "w") as f:
        f.write(testfile)


def write_provider_state_file(
    provider_state_file: str, path: Path, merge=False
) -> ProviderStateFileOutcome:
    # TODO: Support appending new provider state functions.
    # For now, don't write the file if it already exists
    exists = path.exists()
    if exists:
        if merge:
            with open(path, "w") as target_handle:
                target = target_handle.read()
                final = merge(target, provider_state_file)
                target.seek(0)
                target.write(final)
            return ProviderStateFileOutcome.MERGED
        return ProviderStateFileOutcome.LEFT_EXISTING
    with open(path, "w") as f:
        f.write(provider_state_file)
        return ProviderStateFileOutcome.WROTE_NEW


def get_functions(mod: Module) -> Generator[FunctionDef, None, None]:
    for node in mod.body:
        if isinstance(node, FunctionDef):
            yield node


def merge_is_available():
    return unparse is not None


def merge(target: str, src: str) -> str:
    """
    Merge "src" code into "target".

    Only add functions from src that aren't
    already present in target.
    """
    if not merge_is_available:
        raise RuntimeError("Cannot merge. No unparse function available")
    target_ast = parse(target)
    target_buffer = StringIO()
    target_buffer.write(target)
    src_ast = parse(src)
    existing_function_names = set([func.name for func in get_functions(target_ast)])
    function_bodies_to_add: List[str] = []
    for funcdef in get_functions(src_ast):
        if funcdef.name not in existing_function_names:
            function_bodies_to_add.append(unparse(funcdef))

    if function_bodies_to_add:
        target_buffer.write("\n")
        target_buffer.write("\n\n".join(function_bodies_to_add))
        target_buffer.write("\n\n")

    return target_buffer.getvalue()
