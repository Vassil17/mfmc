class RequiredDatafieldError(KeyError):
    """Indicates that a required datafield was not found.

    Parameters
    ----------
    name
        The key name which was attempted to be accesssed.
    """
    def __init__(self, name: str):
        msg = f"Required datafield not found: {name}"
        super().__init__(msg)

class OptionalDatafieldError(KeyError):
    """Indicates that an optional datafield was not found.

    Parameters
    ----------
    name
        The key name which was attempted to be accesssed.
    """
    def __init__(self, name: str):
        msg = f"Optional datafield not found: {name}"
        super().__init__(msg)

class UnknownDatafieldError(KeyError):
    """Indicates that a user-defined datafield was accessed incorrectly.

    User attributes should be accessed using the ``user_attributes`` property,
    and user datasets should be accessed using the ``user_datasets`` property.
    Parameters
    ----------
    name
        The key name which was attempted to be accesssed.
    """
    def __init__(self, name: str):
        msg = f"Unknown datafield not found: {name}"
        super().__init__(self, msg)
