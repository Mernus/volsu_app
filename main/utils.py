STRING_TEMPLATES = {
    "success": "\033[32m [{}SUCCESS]: {} \033[0m",
    "info": "\033[1m [{}INFO]: {} \033[0m",
    "warn": "\033[33m [{}WARNING]: {}\033[0m",
    "err": "\033[31m [{}ERROR]: {}\033[0m"
}


def colored_print(uncolored_string: str, *, string_code: str, path: str = None, critical: bool = False) -> None:
    """
    Modified print function with some color and string code.

    Args:
        uncolored_string (string): String without color and string code
        string_code (string): String codes from STRING_TEMPLATES
        path (string optional): Path or filename to indicate string location
        critical (bool optional): If True raise SystemExit

    """

    template = STRING_TEMPLATES.get(string_code, "")
    filename = path.upper() + " | " if path else ""
    string_template = template.format(filename, uncolored_string)

    if critical:
        raise SystemExit(string_template)

    print(string_template)


def clear_cached_properties(instance, properties: set):
    """
    Clear cache for cached properties of instance.

    Args:
        instance (): Instance that have cached properties
        properties (set): Set of cached properties

    """
    cached_properties = properties & instance.__dict__.keys()

    for prop in cached_properties:
        del instance.__dict__[prop]
