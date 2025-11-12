import sqlite3

def criar_tabela():
    """Cria a tabela pacientes no banco de dados (migração segura)."""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cpf INTEGER,
                data_nascimento DATE,
                observacoes TEXT
            )
        ''')

        conexao.commit()
        conexao.close()

        print("✅ Tabela 'pacientes' criada/verificada!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabela pacientes: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()
