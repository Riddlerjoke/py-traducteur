from fastapi import FastAPI
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

from config.parametres import VERSIONS
from model.nlp import traduire
from model.prompt import Prompt
from dto.servicetraducteur import ServiceTraducteur as st
from model.utilisateur import Utilisateur
from prometheus_client import Summary, Counter
import time
import random

tags = [
    {
        "name": "index",
        "description": "Index"
    },
    {
        "name": "traduction",
        "description": "Traduction"
    },
    {
        "name": "authentification",
        "description": "authentification"
    }
]

app = FastAPI(
    title="Appli de traduction",
    description="API de traudction",
    version="1.0.0",
    openapi_tags=tags
)

# Créez des métriques Prometheus
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNTER = Counter('app_requests_total', 'Total number of requests')

# Instrumentateur Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/")
@REQUEST_TIME.time()
def read_root():
    REQUEST_COUNTER.inc()
    time.sleep(random.random())
    return {"Hello": "World"}


@app.get("/versions", tags=["index"])
def versions():
    return VERSIONS


@app.post("/traductions", tags=["traduction"])
def traducteur(prompt: Prompt):
    traduire(prompt)
    st.sauvegarder_prompt(prompt)
    return prompt


@app.get("/traductions/auteur/{id}", tags=["traduction"])
def versions_par_auteur(id: int):
    return st.lister_prompts(id)


@app.post("/login", tags=["authentification"])
def authentifier(utilisateur: Utilisateur):
    st.verifier_login(utilisateur)
    return {"authentifié": utilisateur.authentifie, "id": utilisateur.id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
