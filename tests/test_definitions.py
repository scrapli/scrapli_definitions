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
