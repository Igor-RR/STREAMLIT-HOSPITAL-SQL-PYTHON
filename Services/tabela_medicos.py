import sqlite3

def criar_tabela():
    """Cria a tabela medicos no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                cpf_medico INTEGER PRIMARY KEY,
                numero_registro TEXT NOT NULL UNIQUE,
                ano_registro TEXT NOT NULL,
                telefone TEXT,
                FOREIGN KEY (cpf_medico) REFERENCES funcionarios_hospital(cpf)
            )
        ''')
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'medicos' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela medicos: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()