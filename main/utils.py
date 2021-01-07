STRING_TEMPLATES = {
    "success": "\033[32m [{}SUCCESS]: {} \033[0m",
    "info": "\033[1m [{}INFO]: {} \033[0m",
    "warn": "\033[33m [{}WARNING]: {}\033[0m",
    "err": "\033[31m [{}ERROR]: {}\033[0m"
}


def colored_print(uncolored_string: str, *, string_code: str, path: str = None, exit: bool = False) -> None:
    """
    Modified print function with some color and string code.

    Args:
        uncolored_string (string): String without color and string code
        string_code (string): String codes from STRING_TEMPLATES
        path (string optional): Path or filename to indicate string location
        exit (bool optional): If True raise SystemExit

    """

    template = STRING_TEMPLATES.get(string_code, "")
    filename = path.upper() + " | " if path else ""
    string_template = template.format(filename, uncolored_string)

    if exit:
        raise SystemExit(string_template)
    else:
        print(string_template)