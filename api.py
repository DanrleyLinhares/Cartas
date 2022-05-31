from typing import List
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import databases
import sqlalchemy

app = FastAPI()

DATABASE_URL = "postgresql://akybyuoiwbxfyv:1c670bb5d549dbfd04b07fdbec8605584dad996226d50b58ef09bdac7d24d423@ec2-3-234-131-8.compute-1.amazonaws.com:5432/d2nmme35a5k893"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "Cartas",
    metadata,
    sqlalchemy.Column("nome", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("edicao", sqlalchemy.String),
    sqlalchemy.Column("idioma", sqlalchemy.String),
    sqlalchemy.Column("foil", sqlalchemy.Boolean),
    sqlalchemy.Column("preco", sqlalchemy.Integer),
    sqlalchemy.Column("quantidade", sqlalchemy.Float),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)



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


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/Pesquisar-carta/", response_model=Carta)
async def pequisar_carta(nome: Optional[str] = None):
    
    query =  notes.select().where(notes.c.nome == nome)

    return await database.fetch_one(query)
    

@app.get("/Listar-Cartas/", response_model=List[Carta])
async def listar_Cartas():
    query = notes.select()
    return await database.fetch_all(query)


@app.put('/Atualizar-carta', response_model=CartaAtualizavel)
async def atualizar_Carta(nome_da_carta: str, carta: CartaAtualizavel):

    query = notes.update().where(notes.c.nome == nome_da_carta).values(preco=carta.preco, 
    quantidade=carta.quantidade)

    await database.execute(query)
    
    return {**carta.dict(), "id": carta}


@app.post("/Criar-Cartas/", response_model=Carta)
async def criar_Cartas(carta: Carta):
    query = notes.insert().values(nome=carta.nome, edicao=carta.edicao, idioma=carta.idioma, 
    foil=carta.foil, preco=carta.preco, quantidade=carta.quantidade)
    last_record_id = await database.execute(query)
    return {**carta.dict(), "id": last_record_id}

@app.delete("/deletar-carta/")
async def deletar_carta(nome_da_carta: str):
    query = notes.delete().where(notes.c.nome == nome_da_carta)
    await database.execute(query)
    return {"Messagem": "A carta deletada com sucesso!"}
