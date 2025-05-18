import re

import pytest

PROMPTS = (
    (
        "simple-exec",
        "exec",
        "csr1000v>",
    ),
    (
        "simple-privileged-exec",
        "privileged_exec",
        "csr1000v#",
    ),
    (
        "privileged-exec-underscore",
        "privileged_exec",
        "csr_1000v#",
    ),
    (
        "simple-configuration",
        "configuration",
        "csr1000v(config)#",
    ),
    (
        "configuration-dashes",
        "configuration",
        "csr1000v(conf-ssh-pubkey-data)#",
    ),
    (
        "configuration-tacacs+",
        "configuration",
        "csr1000v(config-sg-tacacs+)#",
    ),
    (
        "configuration-ipsec-profile",
        "configuration",
        "819HGW(ipsec-profile)#",
    ),
    (
        "simple-tclsh",
        "tclsh",
        "819HGW(tcl)#",
    ),
    (
        "tclsh-+",
        "tclsh",
        "+>",
    ),
    (
        "tclsh-+>",
        "tclsh",
        "+>(tcl)#",
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
