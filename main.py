from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
import logging
from groq import Groq


app = FastAPI()


def executar_prompt(tema: str):
    prompt = f"Escreva uma história sobre o {tema}"
    client = Groq(
        api_key="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)",
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


@app.post("/gerar_historia")
def gerar_historia(tema: str):
    historia = executar_prompt(tema)
    return {"História": historia}
