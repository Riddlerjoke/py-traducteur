from pydantic import BaseModel


class Prompt(BaseModel):
    atraduire: str
    traduction: str
    version: str
    utilisateur: int

