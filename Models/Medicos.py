from dataclasses import dataclass

@dataclass
class Medicos:
    cpf_medico: int  # FK para Funcionario_hospital.cpf_funcionario
    numero_registro: str
    ano_registro: str
    telefone: str
    
