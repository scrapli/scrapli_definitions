import re

import pytest

PROMPTS = (
    (
        "simple",
        "exec",
        "ACME-FIREWALL>",
    ),
    (
        "simple-underscore-trailing-space",
        "exec",
        "ACME_FIREWALL> ",
    ),
    (
        "ha-pair-primary",
        "exec",
        "ACME_FIREWALL/act/pri>",
    ),
    (
        "period-in-hostname",
        "exec",
        "ACME-FIREWALL.local>",
    ),
    (
        "simple",
        "privileged_exec",
        "ACME-FIREWALL#",
    ),
    (
        "context",
        "privileged_exec",
        "SYSCONT/CTX1# ",
    ),
    (
        "ha-pair-secondary-conf",
        "privileged_exec",
        "SYSCONT/CTX1/act/sec# ",
    ),
    (
        "simple",
        "configuration",
        "ACME-FIREWALL(config)#",
    ),
    (
        "interface-config",
        "configuration",
        "ACME-FIREWALL(config-if)#",
    ),
    (
        "config-context-ha",
        "configuration",
        "SYSCONT/CTX1/act/sec(config)#",
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
