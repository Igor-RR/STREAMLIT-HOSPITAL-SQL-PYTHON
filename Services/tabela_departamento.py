# Services/tabela_departamento.py
import sqlite3

def criar_tabela():
    """Cria a tabela departamentos no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                numero_funcionarios INTEGER NOT NULL
            )
        ''')
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'departamentos' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()