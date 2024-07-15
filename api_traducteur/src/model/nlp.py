from transformers import pipeline, Pipeline
from src.config.parametres import VERSIONS
from src.model.prompt import Prompt


def traduire(prompt: Prompt):

    if prompt.version == VERSIONS[0]:
        translator: Pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

    prompt.traduction = translator(prompt.atraduire)
    return prompt