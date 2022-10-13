import requests
from pydantic import parse_raw_as

from discord_utils.schemas import Command, Token

API_ENDPOINT = "https://discord.com/api/v10"
TOKEN_ENDPOINT = f"{API_ENDPOINT}/oauth2/token"


class DiscordClient(requests.Session):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scope: str,
        api_endpoint: str = API_ENDPOINT,
        token_endpoint: str = TOKEN_ENDPOINT,
    ):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.api_endpoint = api_endpoint
        self.token_endpoint = token_endpoint

        self.headers["Authorization"] = f"Bearer {self.auth_token.access_token.get_secret_value()}"

    @property
    def auth_token(self) -> Token:
        data = {"grant_type": "client_credentials", "scope": self.scope}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            self.token_endpoint,
            data=data,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )
        r.raise_for_status()
        return Token.parse_raw(r.content)

    def commands(self) -> list[Command]:
        resp = self.get(f"{self.api_endpoint}/applications/{self.client_id}/commands")
        return parse_raw_as(list[Command], resp.content)

    def add_command(self, data: dict) -> Command:

        resp = self.post(
            f"{self.api_endpoint}/applications/{self.client_id}/commands",
            json=data,
        )
        resp.raise_for_status()
        return Command.parse_raw(resp.content)

    def delete_command(self, id_: str):
        resp = self.delete(
            f"{self.api_endpoint}/applications/{self.client_id}/commands/{id_}",
        )
        resp.raise_for_status()
        return resp
