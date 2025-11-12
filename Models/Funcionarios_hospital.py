from dataclasses import dataclass

@dataclass
class Funcionario_hospital:
    cpf: int
    nome: str
    cargo: str
    id_departamento: int
    data_admissao: str
    salario: float = None