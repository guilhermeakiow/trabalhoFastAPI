from fastapi import FastAPI

app = FastAPI()


@app.get("/teste")
def hello_world():
    return {"mensagem": " Hello World"}


# Criando um endpoint para receber dois números e retornar a soma:


# Passando o número 1 e 2 na URL
@app.get("/soma/{numero1}/{numero2}")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Passando o número 1 e 2 no corpo da requisição


@app.post("/soma_formato2")
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Passando o número 1 e 2 no corpo da requisição
from pydantic import BaseModel


class Numeros(BaseModel):
    numero1: int
    numero2: int


@app.post("/soma_formato3")
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}
