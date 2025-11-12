# Controllers/ObitosController.py
import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Obitos import Obitos

def conectaBD():
    return sqlite3.connect("Hospital.db")

def incluir_obito(obito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações
        if not obito.id_paciente:
            raise ValueError("ID do paciente é obrigatório")
        
        if not obito.id_medico:
            raise ValueError("ID do médico é obrigatório")
        
        if not obito.data_obito or not obito.data_obito.strip():
            raise ValueError("Data do óbito é obrigatória")
        
        if not obito.causa_obito or not obito.causa_obito.strip():
            raise ValueError("Causa do óbito é obrigatória")
        
        cursor.execute('''
            INSERT INTO obitos (id_paciente, id_medico, data_obito, causa_obito, observacoes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            obito.id_paciente,
            obito.id_medico,
            obito.data_obito.strip(),
            obito.causa_obito.strip(),
            obito.observacoes.strip() if obito.observacoes else None
        ))
        
        conexao.commit()
        return True
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro no banco: {e}")
        return False
    finally:
        conexao.close()

def consultar_obitos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM obitos")
        obitos = cursor.fetchall()
        return [Obitos(
            id_obito=row[0],
            id_paciente=row[1],
            id_medico=row[2],  # NOVO CAMPO
            data_obito=row[3],
            causa_obito=row[4],
            observacoes=row[5]
        ) for row in obitos]
    except sqlite3.Error as e:
        print(f"Erro ao consultar: {e}")
        return []
    finally:
        conexao.close()

def consultar_obito_por_id(id_obito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM obitos WHERE id_obito = ?", (id_obito,))
        row = cursor.fetchone()
        if row:
            return Obitos(
                id_obito=row[0],
                id_paciente=row[1],
                id_medico=row[2],  # NOVO CAMPO
                data_obito=row[3],
                causa_obito=row[4],
                observacoes=row[5]
            )
        return None
    except sqlite3.Error as e:
        print(f"Erro ao consultar: {e}")
        return None
    finally:
        conexao.close()

def excluir_obito(id_obito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM obitos WHERE id_obito = ?", (id_obito,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir: {e}")
        return False
    finally:
        conexao.close()

def alterar_obito(obito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações
        if not obito.id_paciente:
            raise ValueError("ID do paciente é obrigatório")
        
        if not obito.id_medico:
            raise ValueError("ID do médico é obrigatório")
        
        if not obito.data_obito or not obito.data_obito.strip():
            raise ValueError("Data do óbito é obrigatória")
        
        if not obito.causa_obito or not obito.causa_obito.strip():
            raise ValueError("Causa do óbito é obrigatória")
        
        cursor.execute('''
            UPDATE obitos 
            SET id_paciente = ?, id_medico = ?, data_obito = ?, causa_obito = ?, observacoes = ?
            WHERE id_obito = ?
        ''', (
            obito.id_paciente,
            obito.id_medico,
            obito.data_obito.strip(),
            obito.causa_obito.strip(),
            obito.observacoes.strip() if obito.observacoes else None,
            obito.id_obito
        ))
        
        conexao.commit()
        return cursor.rowcount > 0
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro no banco: {e}")
        return False
    finally:
        conexao.close()

# NOVA FUNÇÃO: Contar óbitos por médico
def contar_obitos_por_medico():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT id_medico, COUNT(*) as total_obitos
            FROM obitos
            GROUP BY id_medico
        ''')
        resultados = cursor.fetchall()
        # Converter para dicionário: id_medico -> total_obitos
        return {row[0]: row[1] for row in resultados}
    except sqlite3.Error as e:
        print(f"Erro ao contar óbitos por médico: {e}")
        return {}
    finally:
        conexao.close()

def incluir_obito(obito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações
        if not obito.id_paciente:
            raise ValueError("ID do paciente é obrigatório")
        
        if not obito.id_medico:  # NOVO CAMPO
            raise ValueError("ID do médico é obrigatório")
        
        if not obito.data_obito or not obito.data_obito.strip():
            raise ValueError("Data do óbito é obrigatória")
        
        if not obito.causa_obito or not obito.causa_obito.strip():
            raise ValueError("Causa do óbito é obrigatória")
        
        cursor.execute('''
            INSERT INTO obitos (id_paciente, id_medico, data_obito, causa_obito, observacoes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            obito.id_paciente,
            obito.id_medico,  # NOVO CAMPO
            obito.data_obito.strip(),
            obito.causa_obito.strip(),
            obito.observacoes.strip() if obito.observacoes else None
        ))
        
        conexao.commit()
        return True
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro no banco: {e}")
        return False
    finally:
        conexao.close()