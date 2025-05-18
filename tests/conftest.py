from pathlib import Path

import pytest
import yaml
from schema import Definition


@pytest.fixture(scope="function")
def d(request: pytest.FixtureRequest) -> str:
    platform_name = request.path.name.lstrip("test_").rstrip(".py")
    definition_name = Path(f"definitions/{platform_name}.yaml")

    return Definition(**yaml.safe_load(definition_name.read_text()))
