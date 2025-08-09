from scrapli import Cli


def mikrotik_routeros_post_init(c: Cli) -> None:
    c.auth_options.username = f"{c.auth_options.username}+tc"
    c.session_options.return_char = "\r\n"
