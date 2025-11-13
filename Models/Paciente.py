
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Paciente:
    id_paciente: Optional[int] = field(default=None)
    nome: str = ""
    cpf: Optional[int] = None
    data_nascimento: str = ""
    observacoes: str = ""
    # Campos antigos mantidos como opcionais caso sejam usados em outras partes
    rg: Optional[str] = None
    sintomas: Optional[str] = None
    historico_anterior: Optional[str] = None
    cpf_medico: Optional[int] = None
    numero_do_coren: Optional[str] = None
    numero_registro_medico: Optional[str] = None




