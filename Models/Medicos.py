from dataclasses import dataclass

@dataclass
class Medicos:
    cpf_medico: int  # FK para funcionarios_hospital.cpf
    numero_registro: str
    ano_registro: str
    telefone: str