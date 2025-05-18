import re

import pytest

PROMPTS = (
    ("simple-exec", "exec", "boxen> "),
    ("simple-configuration", "configuration", "boxen# "),
    ("exec-underscore", "exec", "box_en> "),
    ("exec-ampersand-period", "exec", "rancid@router2.xyz6> "),
    ("exec-master", "exec", "{master}\nusername@MX-960-PE1>"),
    ("exec-backup", "exec", "{backup}\nusername@MX-480-PE2>"),
    ("exec-primary", "exec", "{primary:node0}\nusername@SRX-4600-FW1>"),
    ("configuration-ampersand-period", "configuration", "rancid@router2.xyz6# "),
    ("configuration-master", "configuration", "{master}[edit]\nusername@MX-960-PE1#"),
    ("configuraiton-backup", "configuration", "{backup}[edit]\nusername@MX-480-PE2#"),
    ("configuration-primary", "configuration", "{primary:node0}[edit]\nusername@SRX-4600-FW1#"),
    ("simple-shell", "shell", "asdfklsdjlf\n%"),
    ("shell-vrf", "shell", "[vrf:foo] regress@EVOvFOOBAR_RE0-re0:~$"),
    ("simple-root-shell", "root_shell", "root@%"),
    ("root-shell-with-path", "root_shell", "root@vMX1_RE:/var/home/regress #"),
    ("root-shell-tilda", "root_shell", "[vrf:foo] root@EVOvFOOBAR_RE0-re0:~#"),
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
