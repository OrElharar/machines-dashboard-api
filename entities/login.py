from pydantic.dataclasses import dataclass


@dataclass
class LoginInputDTO:
    username: str
    password: str


@dataclass
class LoginDTO(LoginInputDTO):
    token: str

