from dataclasses import dataclass

@dataclass
class Funcionario_hospital:
    cpf_funcionario: int  # CHAVE PRIMÁRIA
    nome: str
    cargo: str
    id_departamento: int  # FK





#from dataclasses import dataclass

#@dataclass
#class Produto:
#id: int
#nome: str
#preco: float

