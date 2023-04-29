from pydantic import BaseModel
from typing import List
from model.pessoa import Pessoa


class PessoaSchema(BaseModel):
    id: int = 1
    nome: str = "Nome"
    email: str = "email@email.com"


class PessoaBuscaSchema(BaseModel):
    id: int = 1
    nome: str = "Nome"


class ListagemPessoaSchema(BaseModel):
    pessoas: List[PessoaSchema]


def apresenta_pessoas(pessoas: List[Pessoa]):
    result = []

    for pessoa in pessoas:
        result.append(
            {
                "id": pessoa.id,
                "nome": pessoa.nome,
                "email": pessoa.email,
                "idade": pessoa.idade,
                "cpf": pessoa.cpf
            },
        )

    return {"pessoas": result}


class PessoaViewSchema(BaseModel):
    id: int = 1
    nome: str = "Nome"
    email: str = "email@email.com"
    idade: int = 20
    cpf: str = "00000000000"


class PessoaDelSchema(BaseModel):
    mesage: str
    nome: str


def apresenta_pessoa(pessoa: Pessoa):
    return {
        "id": pessoa.id,
        "nome": pessoa.nome,
        "email": pessoa.email,
        "idade": pessoa.idade,
        "cpf": pessoa.cpf
    }
