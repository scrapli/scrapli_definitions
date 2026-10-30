import re

import pytest

PROMPTS = (
    ("slc9000", "exec", "[SLC9032]>"),
    ("slc9000_sku", "exec", "[SLC9016-16U-16E]> "),
    ("slc8000_hyphen", "exec", "[slc8032-lab]>"),
    ("emg_dotted", "exec", "[EMG8500.example]>"),
    ("underscore", "exec", "[edge_console_01]> "),
)

NOT_PROMPTS = (
    ("no_brackets", "SLC9032>"),
    ("hash", "[SLC9032]#"),
    ("confirm_question", "Do you want to continue? [no] "),
    ("login", "login: "),
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
    assert (
        re.search(pattern=m.prompt_pattern, string=prompt, flags=re.MULTILINE | re.IGNORECASE)
        is not None
    )


@pytest.mark.parametrize(
    argnames=(
        "_",
        "prompt",
    ),
    argvalues=NOT_PROMPTS,
    ids=[case[0] for case in NOT_PROMPTS],
)
def test_global_prompt_pattern_rejects(_, prompt, d):
    assert (
        re.search(pattern=d.prompt_pattern, string=prompt, flags=re.MULTILINE | re.IGNORECASE)
        is None
    )
