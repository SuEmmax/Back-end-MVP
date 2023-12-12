from pydantic import BaseModel
from typing import Optional, List, Tuple, Dict
from model.equipe import Equipe

class EquipeCommitView(BaseModel):
    """ Define como um equipe será retornado.
    """
    id: int = 1
    kks: str = "11HBA00AA01"
    unidade: str = "TG1"
    usina: str="Las Flores"
    equipment: str="valvula manual"
   

class EquipeInserir(BaseModel):
    """ Define como um novo equipe é ingresado para ser inserido no db.
    """
    kks: str = "11HBA00AA501"
    unidade: str = "TG1"
    usina: str="Las Flores"
    equipment: str="valvula manual"



class EquipeBuscar(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    kks: str = "13LBA00CT321"


def apresenta_equipe(equipe: Equipe):
    """ Retorna uma representação do kks seguindo o schema definido em
        EquipeCommitInserido.
    """
    return {
        "id": equipe.id,
        "kks": equipe.kks,
        "unidade": equipe.unidade,
        "usina": equipe.usina,
        "equipment":equipe.equipment
    }



class ListagemEquipes(BaseModel):
    """ Define como uma listagem de equipes será retornada.
    """
    equipes:List[EquipeCommitView]
    
def apresenta_equipes(equipes: List[Equipe]):
    """ Retorna uma representação do equipe seguindo o schema definido em
        EquipeCommitView.
    """
    result = []
    for equipe in equipes:
        result.append({
            "kks": equipe.kks,
            "unidade": equipe.unidade,
            "usina": equipe.usina,
            "equipment": equipe.equipment
        })

    return {"equipes": result}





class EquipeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    kks: str

