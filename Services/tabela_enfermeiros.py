# Services/tabela_enfermeiros.py
import sqlite3

def criar_tabela():
    """Cria a tabela enfermeiros no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enfermeiros (
                cpf_enfermeiro INTEGER PRIMARY KEY,
                numero_coren TEXT NOT NULL UNIQUE,
                ano_registro TEXT NOT NULL,
                FOREIGN KEY (cpf_enfermeiro) REFERENCES funcionario_hospital(cpf_funcionario)
            )
        ''')
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'enfermeiros' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela enfermeiros: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()
