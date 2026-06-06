from dataclasses import dataclass


@dataclass(slots=True)
class LoginDTO:
    email: str
    senha: str
