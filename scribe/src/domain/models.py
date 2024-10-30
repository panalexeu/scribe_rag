class FakeModel:

    def __init__(self, portal_gun: bool, spaceship_name: str):
        self.portal_gun = portal_gun
        self.spaceship_name = spaceship_name

    def __repr__(self):
        return f'FakeModel<portal_gun={self.portal_gun}, spaceship_name={self.spaceship_name}>'

    def meow(self) -> str:
        return f'Meow! My ship is {self.spaceship_name}.'


class ApiKeyCredential:

    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key

    def __repr__(self) -> str:
        return f'ApiKeyCredential<name={self.name}, api_key={self.api_key}>'
