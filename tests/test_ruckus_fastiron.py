import re

import pytest

PROMPTS = (
    (
        "simple",
        "exec",
        "ICX7150-24P Switch>",
    ),
    (
        "with-parens",
        "exec",
        "ICX7150-24P Switch(DEV)>",
    ),
    (
        "ssh-prompt",
        "exec",
        "SSH@ICX7150-24P Switch>",
    ),
    (
        "simple",
        "privileged_exec",
        "ICX7150-24P Switch#",
    ),
    (
        "with-parens",
        "privileged_exec",
        "ICX7150-24P Switch(DEV)#",
    ),
    (
        "ssh-prompt",
        "privileged_exec",
        "SSH@ICX7150-24P Switch#",
    ),
    (
        "simple",
        "configuration",
        "ICX7150-24P Switch(config)#",
    ),
    (
        "with-parens",
        "configuration",
        "ICX7150-24P Switch(DEV)(config)#",
    ),
    (
        "ssh-prompt",
        "configuration",
        "SSH@ICX7150-24P Switch(config)#",
    ),
    (
        "interface",
        "configuration",
        "ICX7150-24P Switch(config-if-e1000-1/1/1)#",
    ),
    (
        "ssh-prompt-interface",
        "configuration",
        "SSH@ICX7150-24P Switch(config-if-e1000-1/1/1)#",
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
