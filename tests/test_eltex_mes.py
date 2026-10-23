import re

import pytest

PROMPTS = (
    # --- base modes ---
    ("exec", "exec", "eltex-mes> "),
    ("privileged_exec", "privileged_exec", "eltex-mes# "),
    ("configuration", "configuration", "eltex-mes(config)# "),
    # --- configuration sub-modes ---
    ("config_if", "configuration", "eltex-mes(config-if)# "),
    ("config_vlan", "configuration", "eltex-mes(config-vlan)# "),
    ("config_erps", "configuration", "eltex-mes(config-erps)# "),
    ("config_line", "configuration", "eltex-mes(config-line)# "),
    ("config_vpcgroup", "configuration", "eltex-mes(config-vpcgroup)# "),
    ("config_keychain", "configuration", "eltex-mes(config-keychain)# "),
    ("config_ip_al", "configuration", "eltex-mes(config-ip-al)# "),
    ("config_mac_al", "configuration", "eltex-mes(config-mac-al)# "),
    ("config_macl", "configuration", "eltex-mes(config-macl)# "),
    ("config_mstp_process", "configuration", "eltex-mes(config-mstp-process)# "),
    ("config_ip", "configuration", "eltex-mes(config-ip)# "),
    ("config_dhcp", "configuration", "eltex-mes(config-dhcp)# "),
    ("router_ospf_process", "configuration", "eltex-mes(router_ospf_process)# "),
    # --- hostname with dash, uppercase ---
    ("hostname_with_dash", "privileged_exec", "eltex-mes-test# "),
    ("uppercase", "privileged_exec", "ELTEX-MES# "),
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
