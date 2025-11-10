# Controllers/EnfermeirosController.py
import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Enfermeiros import Enfermeiros

def conectaBD():
    return sqlite3.connect("Hospital.db")

# FUNÇÃO DE INCLUSÃO REMOVIDA - O CADASTRO É FEITO VIA FUNCIONARIOS

def consultar_enfermeiros():
    """Consulta todos os enfermeiros"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM enfermeiros")
        enfermeiros = cursor.fetchall()
        return [Enfermeiros(
            cpf_enfermeiro=row[0],
            numero_coren=row[1], 
            ano_registro=row[2]
        ) for row in enfermeiros]
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return []
    finally:
        conexao.close()

def consultar_enfermeiro_por_cpf(cpf):
    """Consulta enfermeiro por CPF"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM enfermeiros WHERE cpf_enfermeiro = ?", (cpf,))
        row = cursor.fetchone()
        if row:
            return Enfermeiros(
                cpf_enfermeiro=row[0],
                numero_coren=row[1], 
                ano_registro=row[2]
            )
        return None
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return None
    finally:
        conexao.close()

def excluir_enfermeiro(cpf):
    """Exclui um enfermeiro (apenas da tabela enfermeiros) - Use excluir_funcionario_completo para exclusão completa"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM enfermeiros WHERE cpf_enfermeiro = ?", (cpf,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir: {e}")
        return False
    finally:
        conexao.close()

def alterar_enfermeiro(enfermeiro):
    """Altera um enfermeiro existente"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not enfermeiro.numero_coren or not enfermeiro.numero_coren.strip():
            raise ValueError("Número COREN do enfermeiro é obrigatório")
        
        if not enfermeiro.ano_registro or not enfermeiro.ano_registro.strip():
            raise ValueError("Ano de registro do enfermeiro é obrigatório")
        
        cursor.execute('''
            UPDATE enfermeiros 
            SET numero_coren = ?, ano_registro = ?
            WHERE cpf_enfermeiro = ?
        ''', (
            enfermeiro.numero_coren.strip(),
            enfermeiro.ano_registro.strip(),
            enfermeiro.cpf_enfermeiro
        ))
        
        conexao.commit()
        return cursor.rowcount > 0
    except ValueError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        print(f"❌ Erro no banco: {e}")
        return False
    finally:
        conexao.close()

def buscar_enfermeiros_por_coren(numero_coren):
    """Busca enfermeiros por número COREN"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM enfermeiros WHERE numero_coren LIKE ?", (f'%{numero_coren}%',))
        enfermeiros = cursor.fetchall()
        return [Enfermeiros(
            cpf_enfermeiro=row[0],
            numero_coren=row[1], 
            ano_registro=row[2]
        ) for row in enfermeiros]
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()

def consultar_enfermeiros_com_departamento():
    """Consulta enfermeiros com JOIN nas informações do departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                e.cpf_enfermeiro, e.numero_coren, e.ano_registro,
                f.nome, f.cargo, f.id_departamento,
                d.nome as nome_departamento
            FROM enfermeiros e
            INNER JOIN funcionario_hospital f ON e.cpf_enfermeiro = f.cpf_funcionario
            LEFT JOIN departamentos d ON f.id_departamento = d.id
        ''')
        resultados = cursor.fetchall()
        
        enfermeiros_completos = []
        for row in resultados:
            enfermeiro = {
                'cpf_enfermeiro': row[0],
                'numero_coren': row[1],
                'ano_registro': row[2],
                'nome': row[3],
                'cargo': row[4],
                'id_departamento': row[5],
                'nome_departamento': row[6]
            }
            enfermeiros_completos.append(enfermeiro)
        
        return enfermeiros_completos
    except sqlite3.Error as e:
        print(f"Erro ao consultar enfermeiros com departamento: {e}")
        return []
    finally:
        conexao.close()