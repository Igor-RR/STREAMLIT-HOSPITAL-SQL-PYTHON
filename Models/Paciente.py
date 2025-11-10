#ok
from dataclasses import dataclass

@dataclass
class Paciente():
    nome: str
    rg: str
    data_nascimento: str
    sintomas: str
    historico_anterior: str
    cpf: int
    cpf_medico:int
    numero_do_coren: str
    numero_registro_medico: str




