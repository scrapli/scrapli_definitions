import re

import pytest

PROMPTS = (
    (
        "simple",
        "bash",
        "A:srl# ",
    ),
    (
        "simple-exec",
        "exec",
        "--{ running }--[  ]--\nA:srl#",
    ),
    (
        "exec-config-not-saved",
        "exec",
        "--{ + running }--[  ]--\nA:srl#",
    ),
    (
        "exec-factory-and-yang-reload",
        "exec",
        "--{ [YANG RELOAD] [FACTORY] running }--[  ]--\nA:r2# ",
    ),
    (
        "exec-old-startup",
        "exec",
        "--{ [OLD STARTUP] running }--[  ]--\nA:r2# ",
    ),
    (
        "configuration-exclusive",
        "configuration",
        "--{ candidate shared-exclusive default }--[  ]--\nA:srl#",
    ),
    (
        "configuration-with-path",
        "configuration",
        "--{ candidate shared-exclusive default }--[ platform ]--\nA:srl#",
    ),
    (
        "configuration-private",
        "configuration",
        "--{ [FACTORY] candidate private private-root }--[  ]--\nA:r2# ",
    ),
    (
        "configuration-uncommited-changes",
        "configuration",
        "--{ [FACTORY] * candidate private private-root }--[  ]--\nA:r2# ",
    ),
    (
        "simple-configuration",
        "configuration",
        "--{ + candidate shared default }--[  ]--\nA:r2# ",
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
