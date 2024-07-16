from src.config.parametres import VERSIONS
from src.model.prompt import Prompt
from transformers import pipeline


def traduire(prompt: Prompt):

    if prompt.version == VERSIONS[0]:
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
    elif prompt.version == VERSIONS[1]:
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

    prompt.traduction = translator(prompt.atraduire)
    return prompt