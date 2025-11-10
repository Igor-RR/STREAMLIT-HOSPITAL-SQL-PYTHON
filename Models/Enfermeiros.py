from dataclasses import dataclass

@dataclass
class Enfermeiros:
    cpf_enfermeiro: int  # FK para Funcionario_hospital.cpf_funcionario
    numero_coren: str
    ano_registro: str
