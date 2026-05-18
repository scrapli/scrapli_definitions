from pathlib import Path

import pytest
import yaml
from schema import Definition

definitions = list(Path("definitions").glob("*.yaml"))


@pytest.mark.parametrize(
    argnames="d",
    argvalues=definitions,
    ids=[d.name for d in definitions],
)
def test_schema(d):
    Definition.model_validate(yaml.safe_load(d.read_text()))


@pytest.mark.parametrize(
    argnames="d",
    argvalues=definitions,
    ids=[d.name for d in definitions],
)
def test_referenced_modes_exist(d):
    definition = Definition.model_validate(yaml.safe_load(d.read_text()))
    mode_names = {mode.name for mode in definition.modes}

    assert definition.default_mode in mode_names

    for instructions in (definition.on_open_instructions, definition.on_close_instructions):
        for instruction in instructions or []:
            if instruction.enter_mode is not None:
                assert instruction.enter_mode.requested_mode in mode_names
