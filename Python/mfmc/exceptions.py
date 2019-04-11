class RequiredDatafieldError(KeyError):
    def __init__(self, name):
        msg = f"Required datafield not found: {name}"
        super().__init__(msg)

class OptionalDatafieldError(KeyError):
    def __init__(self, name):
        msg = f"Optional datafield not found: {name}"
        super().__init__(msg)
