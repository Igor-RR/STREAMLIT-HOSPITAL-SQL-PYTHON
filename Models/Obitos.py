from dataclasses import dataclass

@dataclass
class Obitos:
    id_obito: int
    id_paciente: int
    id_medico: int
    data_obito: str
    causa_obito: str
    observacoes: str