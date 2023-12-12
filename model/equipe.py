from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base

class Equipe(Base):
    __tablename__ = 'equipe'

    id = Column("pk_equipe", Integer, primary_key=True)
    kks = Column(String(150), unique=True)
    unidade = Column(String(150))
    usina = Column(String(150))
    equipment=Column(String(150))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.


    def __init__(self, kks:str, unidade:str, usina:str, equipment:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            kks: kks do produto.
            unidade: unidade que se espera comprar daquele produto
            usina: usina esperado para o produto
            data_insercao: data de quando o produto foi inserido à base
        """
        self.kks = kks
        self.unidade = unidade
        self.usina = usina
        self.equipment=equipment

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
    