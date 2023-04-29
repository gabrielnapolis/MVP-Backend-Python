from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote
from flask import request

from sqlalchemy.exc import IntegrityError

from model import Session, Pessoa
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
pessoa_tag = Tag(
    name="Pessoa",
    description="Adição, visualização e remoção de pessoas",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


@app.post(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_pessoa():
    """Adiciona uma pessoa à base de dados."""
    content: PessoaSchema = request.get_json()

    if "nome" in content and "email" in content:
        if len(content["nome"]) == 0 | len(content["email"]) == 0:
            error_msg = "Nome e Email devem ser preenchidos"
            return {"mesage": error_msg}, 409

        pessoa = Pessoa(
            nome=content["nome"],
            email=content["email"],
            idade=content["idade"],
            cpf=content["cpf"]
        )

        try:
            session = Session()
            session.add(pessoa)
            session.commit()
            return apresenta_pessoa(pessoa), 200

        except IntegrityError as e:
            error_msg = "Pessoa de mesmo nome já salvo na base"
            return {"mesage": error_msg}, 409

        except Exception as e:
            error_msg = "Não foi possível salvar novo item"
            return {"mesage": error_msg}, 400
    else:
        error_msg = "Nome e Email devem ser preenchidos"
        return {"mesage": error_msg}, 409


@app.get(
    "/pessoas",
    tags=[pessoa_tag],
    responses={"200": ListagemPessoaSchema, "404": ErrorSchema},
)
def get_pessoas():
    """Faz a busca por todas as Pessoas cadastradas

    Retorna uma representação da listagem de pessoas.
    """
    session = Session()
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        return {"pessoas": []}, 200
    else:
        return apresenta_pessoas(pessoas), 200


@app.route(
    "/pessoa/<pessoa_id>",
    methods=["GET"],
)
def get_pessoa(pessoa_id):
    """Faz a busca por uma Pessoa a partir do id

    Retorna uma representação das pessoas e treinos associados.
    """
    session = Session()
    pessoa = session.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

    if not pessoa:
        error_msg = "Pessoa não encontrada da base"
        return {"mesage": error_msg}, 404
    else:
        return apresenta_pessoa(pessoa), 200


@app.route(
    "/pessoa/<pessoa_id>", 
    methods=["DELETE"],
)
def del_pessoa(pessoa_id):
    """Deleta uma Pessoa a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    session = Session()
    pessoa = session.query(Pessoa).filter(Pessoa.id == pessoa_id).delete()
    session.commit()

    if pessoa:
        return {"mesage": "Pessoa removida", "id": pessoa_id}
    else:
        error_msg = "Pessoa não encontrada na base"
        return {"mesage": error_msg}, 404
