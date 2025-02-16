from fastapi import FastAPI, status, HTTPException, Depends
from enum import Enum
import logging
from groq import Groq
import os
from dotenv import load_dotenv

API_TOKEN = 123


# Função chamada de Token API
def verificacaoAPI(api_token: int):
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="API Token inválido")
    return {"api_token": api_token}


# Logs de Erro
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("fastapi")


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Descrição da API
# Esta API foi desenvolvida para gerar histórias com base em estilo e tema. E extrair sentimentos de uma história.
description = """
API desenvolvida para criação de histórias e extração de sentimentos.

- /v1/gerador_de_historias
  - Passo 1 - Selecione o Estilo da História: Aventura, Guerra ou Terror;
  - Passo 2 - Digite o Tema da História;
  - Passo 3 - Clique em Executar.

- /v1/extrator_de_sentimentos
  - Passo 1 - Copie e cole a História gerada;
  - Passo 2 - Clique em Executar.
"""

# Criação da instância do FastAPI
app = FastAPI(
    title="Trabalho API - UFG",
    description=description,
    version="0.1",
    license_info={
        "name": "Alunos: Luis Guimarães e Ricardo Guimarães",
    },
)


# Função para gerar uma história com base no estilo e tema
# Utiliza o modelo de IA para criar a história
def executar_prompt_historia(estilo: str, tema: str):
    prompt = f"Escreva uma história de {estilo} sobre: {tema}"
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),  # Obtém a chave da API do ambiente
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",  # Define o modelo de IA utilizado
    )

    return chat_completion.choices[0].message.content  # Retorna o conteúdo gerado


# Função para extrair sentimentos da história
def extrator_sentimento(historia: str):
    prompt = f"Descreva os sentimentos dessa história: {historia}"
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
        model="llama-3.1-8b-instant",  # IA utilizada
    )

    return chat_completion.choices[
        0
    ].message.content  # Retorna os sentimentos extraídos


# Definição do Enum para os estilos de história possíveis
class EstiloHistoria(str, Enum):
    Aventura = "Aventura"
    Guerra = "Guerra"
    Terror = "Terror"


# Token da API para autenticação
# API_TOKEN = 123


# Endpoint para gerar histórias
@app.post(
    "/v1/gerador_de_historias/{api_token}",
    summary="Retorna uma história",
    tags=["Gerador de Histórias"],
    dependencies=[Depends(verificacaoAPI)],
)
def criar_história(Estilo: EstiloHistoria, Tema: str):

    # Valida se o tema não é composto apenas por números
    if Tema.isdigit():
        logger.error("Não é permitido números negativos")  # Log de controle no terminal
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido somente números como Tema",
        )

    print(
        f"Parametro recebidos com sucesso. Estilo:{Estilo} e Tema:{Tema}"
    )  # Log de controle no terminal

    # Gera a história com base no estilo e tema fornecidos
    historia = executar_prompt_historia(Estilo, Tema)
    return {"História": historia}  # Retorna a história gerada


# Endpoint para extrair sentimentos de uma história
@app.post(
    "/v1/extrator_de_sentimento/{api_token}",
    summary="Retorna sentimentos de uma história",
    tags=["Extrator de Sentimentos"],
)
def extrair_sentimentos(api_token: int, Historia: str):
    # Verifica se o token da API é válido
    if api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API Token inválido"
        )

    # Valida se a história não é composta apenas por números
    if Historia.isdigit():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido somente números como História",
        )

    # Extrai os sentimentos associados à história fornecida
    historia = extrator_sentimento(Historia)
    return {"Sentimentos": historia}  # Retorna os sentimentos extraidos
