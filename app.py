#from model import*
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect

from model import Session, Equipe
from schemas.equipe import *
from schemas.error import *


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Equipe", description="Adição, visualização e remoção de equipes à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')



@app.get('/equipes', tags=[produto_tag],
         responses={"200": ListagemEquipes, "404": ErrorSchema})
def get_equipes():
    """Faz a busca por todos os equipes cadastrados

    Retorna uma representação da listagem de equipes.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    equipes = session.query(Equipe).all()

    if not equipes:
        # se não há equipes cadastrados
        return {"equipes": []}, 200
    else:
        # retorna a representação de equipe
        print(equipes)
        return apresenta_equipes(equipes), 200
    


@app.post('/equipe', tags=[produto_tag],
          responses={"200": EquipeCommitView, "409": ErrorSchema, "400": ErrorSchema})
def add_equipe(form: EquipeInserir):
    """Adiciona um novo Equipe à base de dados

    Retorna uma representação dos Equipes e comentários associados.
    """
    equipe = Equipe(
        kks=form.kks,
        unidade=form.unidade,
        usina=form.usina,
        equipment=form.equipment)

    try:
        # criando conexão com a base
        session = Session()
        # adicionando un equipe
        session.add(equipe)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_equipe(equipe), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Equipe de mesmo kks já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    

@app.get('/equipe', tags=[produto_tag],
         responses={"200": EquipeCommitView, "404": ErrorSchema})
def get_equipe(query: EquipeBuscar):
    """Faz a busca do equipe a partir do kks

    Retorna uma representação dos equipes.
    """
    kks = query.kks.upper()
    # upper é usado para fazer a busca ainda o kks a buscar é digitado en lower
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    equipe = session.query(Equipe).filter(Equipe.kks == kks).first()

    if not equipe:
        # se o equipe não foi encontrado
        error_msg = "equipe não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de equipe
        return apresenta_equipe(equipe), 200


@app.delete('/equipe', tags=[produto_tag],
            responses={"200": EquipeDelSchema, "404": ErrorSchema})
def del_produto(query: EquipeBuscar):
    """Deleta um equipe a partir do kks informado

    Retorna uma mensagem de confirmação da remoção.
    """
    equipe_kks = query.kks.upper()
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Equipe).filter(Equipe.kks == equipe_kks).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Equipe removido", "kks": equipe_kks}
    else:
        # se o equipe não foi encontrado
        error_msg = "Equipe não encontrado na base :/"
        return {"mesage": error_msg}, 404