from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
import logging
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


description = """
API desenvolvida para criação e resumo de histórias.
- /v1/gerador_de_historias
- Passo 1 - Selecione o Estilo da História: Aventura, Guerra ou Terror.
- Passo 2 - Digite o Tema da História”
"""
app = FastAPI(
    title="Trabalho API - UFG",
    description=description,
    version="0.1",
    license_info={
        "name": "Alunos: Luis Guimarães e Ricardo Guimarães",
    },
)


def executar_prompt(estilo: str, tema: str):
    prompt = f"Escreva uma história de {estilo} sobre: {tema}"
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
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


API_TOKEN = 123


@app.post(
    "/v1/gerador_de_historias/{api_token}",
    summary="Retorna uma história",
    tags=["Gerador de Histórias"],
)
def criar_história(api_token: int, Estilo: EstiloHistoria, Tema: str):
    if api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API Token inválido"
        )

    if Tema.isdigit():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido somente números como Tema",
        )

    historia = executar_prompt(Estilo, Tema)
    return {"História": historia}
