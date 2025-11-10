# Services/tabela_funcionario_hospital.py
import sqlite3

def criar_tabela():
    """Cria a tabela funcionario_hospital no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionario_hospital (
                cpf_funcionario INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                id_departamento INTEGER NOT NULL,
                FOREIGN KEY (id_departamento) REFERENCES departamentos(id)
            )
        ''')
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'funcionario_hospital' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela funcionario_hospital: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()