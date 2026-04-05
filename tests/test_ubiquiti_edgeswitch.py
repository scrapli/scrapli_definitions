import re

import pytest

PROMPTS = (
    (
        "exec",
        "exec",
        "(sw-whatever) >",
    ),
    (
        "privileged_exec",
        "privileged_exec",
        "(sw-whatever) #",
    ),
    (
        "configuration",
        "configuration",
        "(sw-whatever) (Config)#",
    ),
    (
        "configuration-interface",
        "configuration",
        "(sw-whatever) (Interface 0/1)#",
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


def test_exec_to_privileged_exec_requires_prompted_input(d):
    exec_mode = next((m for m in d.modes if m.name == "exec"), None)
    assert exec_mode is not None
    assert exec_mode.accessible_modes is not None

    transition = next(
        (am for am in exec_mode.accessible_modes if am.name == "privileged_exec"), None
    )
    assert transition is not None
    assert transition.instructions[0].send_prompted_input is not None
