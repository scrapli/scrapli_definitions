import re

import pytest

PROMPTS = (
    (
        "simple-exec",
        "exec",
        "switch>",
    ),
    (
        "simple-privileged-exec",
        "privileged_exec",
        "switch# ",
    ),
    (
        "simple-configuration",
        "configuration",
        "switch(config)# ",
    ),
    (
        "configuration-interface",
        "configuration",
        "switch(config-if)# ",
    ),
    (
        "configuration-sub-interface",
        "configuration",
        "switch(config-subif)# ",
    ),
    (
        "configuration-vpc-domain",
        "configuration",
        "switch(config-vpc-domain)# ",
    ),
    (
        "configuration-router",
        "configuration",
        "switch(config-router)# ",
    ),
    (
        "configuration-tacacs+",
        "configuration",
        "switch(config-tacacs+)# ",
    ),
    (
        "configuration-tm-dest",
        "configuration",
        "switch(conf-tm-dest)# ",
    ),
    (
        "privilegedexec-underscore",
        "privileged_exec",
        "swi_tch# ",
    ),
    (
        "simple-tclsh",
        "tclsh",
        "switch-tcl# ",
    ),
    (
        "tclsh-non-privileged",
        "tclsh",
        "> ",
    ),
    (
        "privileged-exec-maintenance-mode",
        "privileged_exec",
        "switch(maint-mode)# ",
    ),
    (
        "configuration-maintenance-mode",
        "configuration",
        "switch(maint-mode)(config)# ",
    ),
    (
        "configuration-maintenance-mode-interface",
        "configuration",
        "switch(maint-mode)(config-if)# ",
    ),
    (
        "configuration-maintenance-mode-sub-interface",
        "configuration",
        "switch(maint-mode)(config-subif)# ",
    ),
    (
        "configuration-maintenance-mode-router",
        "configuration",
        "switch(maint-mode)(config-router)# ",
    ),
    (
        "configuration-maintenance-mode-tacacs+",
        "configuration",
        "switch(maint-mode)(config-tacacs+)# ",
    ),
    (
        "configuration-maintenance-mode-tm-dest",
        "configuration",
        "switch(maint-mode)(conf-tm-dest)# ",
    ),
    (
        "tclsh-maintenance-mode",
        "tclsh",
        "switch(maint-mode-tcl)# ",
    ),
    (
        "configuration-maintenance-mode-tclsh",
        "configuration",
        "switch(maint-mode)(config-tcl)# ",
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
