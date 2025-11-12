import sqlite3

def criar_tabela():
    """Cria a tabela obitos no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS obitos (
                id_obito INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                id_medico INTEGER NOT NULL,  -- NOVO CAMPO
                data_obito DATE NOT NULL,
                causa_obito TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
                FOREIGN KEY (id_medico) REFERENCES medicos(cpf_medico)  -- RELAÇÃO COM MÉDICOS
            )
        ''')
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'obitos' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela obitos: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()