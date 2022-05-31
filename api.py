from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

cartas = []

class Carta(BaseModel):
    nome: str
    edicao: str
    idioma: str
    foil: bool
    preco: float
    quantidade: int


class CartaAtualizavel(BaseModel):
    preco: Optional[float] = None
    quantidade: Optional[int] = None

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.get('/Pesquisar-carta')
def pequisar_carta(nome: Optional[str] = None):

    search = list(filter(lambda x: x["nome"] == nome, cartas))

    if search == []:
        return {'Carta': 'Não existe'}

    return {'Carta': search[0]}


@app.get('/Listar-cartas')
def listar():
    return {'Cartas': cartas}


@app.post('/Criar-carta')
def criar_carta(nome_da_carta: str, carta: Carta):

    search = list(filter(lambda x: x["nome"] == nome_da_carta, cartas))

    if search != []:
        return {'Error': 'Já existe.'}

    carta = carta.dict()
    carta['nome'] = nome_da_carta

    cartas.append(carta)
    return carta


@app.put('/Atualizar-carta')
def Atualizar_Carta(nome_da_carta: str, carta: CartaAtualizavel):

    search = list(filter(lambda x: x["nome"] == nome_da_carta, cartas))

    if search == []:
        return {'Carta': 'Não existe'}

    if carta.quantidade is not None:
        search[0]['quantidade'] = carta.quantidade

    if carta.preco is not None:
        search[0]['preco'] = carta.preco
    

    return search


@app.delete('/deletar-carta')
def Deletar_carta(nome_da_carta: str):
    search = list(filter(lambda x: x["nome"] == nome_da_carta, cartas))

    if search == []:
        return {'carta': 'Não existe'}

    for i in range(len(cartas)):
        if cartas[i]['nome'] == nome_da_carta:
            del cartas[i]
            break
    return {'Message': 'carta deletada com sucesso!'}