# Controllers/MedicosController.py
import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Medicos import Medicos

def conectaBD():
    return sqlite3.connect("Hospital.db")

# FUNÇÃO DE INCLUSÃO REMOVIDA - O CADASTRO É FEITO VIA FUNCIONARIOS

def consultar_medicos():
    """Consulta todos os médicos"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM medicos")
        medicos = cursor.fetchall()
        return [Medicos(
            cpf_medico=row[0],
            numero_registro=row[1], 
            ano_registro=row[2],
            telefone=row[3]
        ) for row in medicos]
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return []
    finally:
        conexao.close()

def consultar_medico_por_cpf(cpf):
    """Consulta médico por CPF"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM medicos WHERE cpf_medico = ?", (cpf,))
        row = cursor.fetchone()
        if row:
            return Medicos(
                cpf_medico=row[0],
                numero_registro=row[1], 
                ano_registro=row[2],
                telefone=row[3]
            )
        return None
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return None
    finally:
        conexao.close()

def excluir_medico(cpf):
    """Exclui um médico (apenas da tabela medicos) - Use excluir_funcionario_completo para exclusão completa"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM medicos WHERE cpf_medico = ?", (cpf,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir: {e}")
        return False
    finally:
        conexao.close()

def alterar_medico(medico):
    """Altera um médico existente"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not medico.numero_registro or not medico.numero_registro.strip():
            raise ValueError("Número de registro do médico é obrigatório")
        
        if not medico.ano_registro or not medico.ano_registro.strip():
            raise ValueError("Ano de registro do médico é obrigatório")
        
        cursor.execute('''
            UPDATE medicos 
            SET numero_registro = ?, ano_registro = ?, telefone = ?
            WHERE cpf_medico = ?
        ''', (
            medico.numero_registro.strip(),
            medico.ano_registro.strip(),
            medico.telefone.strip() if medico.telefone else None,
            medico.cpf_medico
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

def buscar_medicos_por_registro(numero_registro):
    """Busca médicos por número de registro"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM medicos WHERE numero_registro LIKE ?", (f'%{numero_registro}%',))
        medicos = cursor.fetchall()
        return [Medicos(
            cpf_medico=row[0],
            numero_registro=row[1], 
            ano_registro=row[2],
            telefone=row[3]
        ) for row in medicos]
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()

def consultar_medicos_com_departamento():
    """Consulta médicos com JOIN nas informações do departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                m.cpf_medico, m.numero_registro, m.ano_registro, m.telefone,
                f.nome, f.cargo, f.id_departamento,
                d.nome as nome_departamento
            FROM medicos m
            INNER JOIN funcionario_hospital f ON m.cpf_medico = f.cpf_funcionario
            LEFT JOIN departamentos d ON f.id_departamento = d.id
        ''')
        resultados = cursor.fetchall()
        
        medicos_completos = []
        for row in resultados:
            medico = {
                'cpf_medico': row[0],
                'numero_registro': row[1],
                'ano_registro': row[2],
                'telefone': row[3],
                'nome': row[4],
                'cargo': row[5],
                'id_departamento': row[6],
                'nome_departamento': row[7]
            }
            medicos_completos.append(medico)
        
        return medicos_completos
    except sqlite3.Error as e:
        print(f"Erro ao consultar médicos com departamento: {e}")
        return []
    finally:
        conexao.close()