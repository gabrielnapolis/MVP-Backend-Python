from sqlalchemy import Column, String, Integer

from model import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    email = Column(String(140))
    idade = Column(Integer)
    cpf = Column(String(140))

    def __init__(
        self,
        nome: str,
        email: str,
        idade: int,
        cpf: str
    ):
        self.nome = nome
        self.email = email
        self.idade = idade
        self.cpf = cpf
