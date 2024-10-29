class ApiKeyCredential:

    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key

    def __repr__(self) -> str:
        return f'ApiKeyCredential(name={self.name}, api_key={self.api_key})'
