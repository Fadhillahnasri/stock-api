class ProviderError(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProviderTimeoutError(ProviderError):
    pass


class ProviderConnectionError(ProviderError):
    pass