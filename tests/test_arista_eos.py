import re

import pytest

PROMPTS = (
    (
        "simple-exec",
        "exec",
        "localhost>",
    ),
    (
        "exec-with-parens",
        "exec",
        "localhost(something)>",
    ),
    (
        "exec-with-spaces",
        "exec",
        "localhost(some thing)>",
    ),
    (
        "simple-privileged-exec",
        "privileged_exec",
        "localhost#",
    ),
    (
        "privileged-exec-with-parens",
        "privileged_exec",
        "localhost(something)#",
    ),
    (
        "privileged-exec-with-spaces",
        "privileged_exec",
        "localhost(some thing)#",
    ),
    (
        "simple-configuration",
        "configuration",
        "localhost(config)#",
    ),
    (
        "configuration-with-parens",
        "configuration",
        "localhost(something)(config)#",
    ),
    (
        "configuration-with-spaces",
        "configuration",
        "localhost(some thing)(config)#",
    ),
    (
        "configuration-with-session",
        "configuration",
        "localhost(some thing)(config-s-tacocat)#",
    ),
    (
        "configuration-with-long-qos-profile",
        "configuration",
        "eos_switch(config-s-scrapl-qos-profile-CORE-EGRESS-QUEUING-txq-5)#",
    ),
    (
        "configuration-with-tacacs+",
        "configuration",
        "eos_switch(config-sg-tacacs+-my_group)#",
    ),
    (
        "configuration-session-with-tacacs+",
        "configuration",
        "eos_switch(config-s-sc-sg-tacacs+-my_group)#",
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


@pytest.mark.parametrize(
    argnames=("prompt",),
    argvalues=(("some stuff in show tech output <redacted>",),),
    ids=("dont-match-on-show-tech-output",),
)
def test_global_prompt_pattern_negative(prompt, d):
    assert (
        re.search(pattern=d.prompt_pattern, string=prompt, flags=re.MULTILINE | re.IGNORECASE)
        is None
    )
