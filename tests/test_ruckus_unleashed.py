import re

import pytest

PROMPTS = (
    (
        "simple",
        "exec",
        "ruckus> ",
    ),
    (
        "simple-short",
        "exec",
        "foo> ",
    ),
    (
        "simple",
        "privileged_exec",
        "ruckus# ",
    ),
    (
        "simple-short",
        "privileged_exec",
        "foo# ",
    ),
    (
        "simple",
        "configuration",
        "ruckus(config)# ",
    ),
    (
        "simple-short",
        "configuration",
        "foo(config)# ",
    ),
    (
        "interface",
        "configuration",
        "ruckus(config-sys-if)# ",
    ),
    (
        "interface-short",
        "configuration",
        "foo(config-sys-if)# ",
    ),
    (
        "simple",
        "debug",
        "ruckus(debug)# ",
    ),
    (
        "simple-short",
        "debug",
        "foo(debug)# ",
    ),
)


@pytest.mark.parametrize(
    argnames=(
        "_",
        "__",
        "prompt",
    ),
    argvalues=PROMPTS,
    ids=[case[0] for case in PROMPTS],
)
def test_global_prompt_pattern(_, __, prompt, d):
    assert (
        re.search(pattern=d.prompt_pattern, string=prompt, flags=re.MULTILINE | re.IGNORECASE)
        is not None
    )


@pytest.mark.parametrize(
    argnames=(
        "_",
        "mode",
        "prompt",
    ),
    argvalues=PROMPTS,
    ids=[case[0] for case in PROMPTS],
)
def test_mode_prompt_patterns(_, mode, prompt, d):
    m = next((found_mode for found_mode in d.modes if found_mode.name == mode), None)

    assert m is not None

    if m.prompt_exact:
        assert prompt in m.prompt_exact
    else:
        assert (
            re.search(pattern=m.prompt_pattern, string=prompt, flags=re.MULTILINE | re.IGNORECASE)
            is not None
        )
