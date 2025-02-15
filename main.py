from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
import logging
from groq import Groq


app = FastAPI()


def executar_prompt(estilo: str, tema: str):
    prompt = f"Escreva uma história de {estilo} sobre: {tema}"
    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content


class EstiloHistoria(str, Enum):
    Aventura = "Aventura"
    Emocionante = "Guerra"
    Terror = "Terror"


@app.post("/v1/criador_de_historias", tags=["Criador de Histórias"])
def criar_história(Estilo: EstiloHistoria, Tema: str):
    historia = executar_prompt(Estilo, Tema)
    return {"História": historia}
