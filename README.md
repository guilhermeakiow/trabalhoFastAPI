## Trabalho da disciplina de API para Pós Graduação em Sistemas e Agentes Inteligentes - Prof. Rogério Rodrigues

## Orientações para executar a API de Criação de Histórias e extração de sentimentos.

- Crie um ambiente virtual: `python -m venv venv`
- Ative o ambiente virtual (no Windows): `venv\Scripts\activate`
- Ative o ambiente virtual (no Linux): `source venv/bin/activate`
- Instale as bibliotecas: `pip install -r requirements.txt`
- Executar a API em ambiente de desenvolvimento:
`fastapi dev main.py`
- Executar a API em ambiente de produção: `fastapi run main.py`
- Se tiver algum erro no pydantic_core, reinstale-o de acordo com sua arquitetura.
    -Comando para reinstalação: `pip uninstall pydantic_core`
                   `pip install --no-cache-dir --force-reinstall pydantic`
- No navegador digitar: `http://127.0.0.1:8000/docs#/` e seguir o passo a passo informado.

