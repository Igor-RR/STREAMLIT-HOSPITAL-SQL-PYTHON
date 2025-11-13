import sqlite3

def conectaBD():
    return sqlite3.connect("Hospital.db")

def criar_tabela_pacientes():
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf INTEGER,
            data_nascimento TEXT,
            observacoes TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def inserir_paciente(nome, cpf, data_nascimento, observacoes):
    try:
        conexao = conectaBD()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nome, cpf, data_nascimento, observacoes) VALUES (?, ?, ?, ?)",
            (nome, cpf, data_nascimento, observacoes)
        )
        conexao.commit()
        conexao.close()
        return True
    except Exception as e:
        print(f"Erro ao inserir paciente: {e}")
        return False

def consultar_pacientes():
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_paciente, nome, cpf, data_nascimento, observacoes FROM pacientes")
    rows = cursor.fetchall()
    conexao.close()
    return rows


def cpf_existe(cpf):
    """Retorna True se já existir paciente com o CPF informado."""
    try:
        conexao = conectaBD()
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM pacientes WHERE cpf = ? LIMIT 1", (cpf,))
        encontrado = cursor.fetchone() is not None
        conexao.close()
        return encontrado
    except Exception as e:
        print(f"Erro ao checar CPF: {e}")
        return False

def excluir_paciente(id_paciente):
    try:
        conexao = conectaBD()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id_paciente = ?", (id_paciente,))
        conexao.commit()
        deleted = cursor.rowcount
        conexao.close()
        return deleted > 0
    except Exception as e:
        print(f"Erro ao excluir paciente: {e}")
        return False

# Garante que a tabela exista ao importar o módulo
criar_tabela_pacientes()
