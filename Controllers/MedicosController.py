import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Medicos import Medicos

def conectaBD():
    return sqlite3.connect("Hospital.db")

def incluir_medico(medico):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO medicos (cpf_medico, numero_registro, ano_registro, telefone)
            VALUES (?, ?, ?, ?)
        ''', (
            medico.cpf_medico,
            medico.numero_registro,
            medico.ano_registro,
            medico.telefone
        ))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao incluir médico: {e}")
        return False
    finally:
        conexao.close()

def consultar_medicos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM medicos")
        resultados = cursor.fetchall()
        medicos = []
        for row in resultados:
            medicos.append(Medicos(
                cpf_medico=row[0],
                numero_registro=row[1],
                ano_registro=row[2],
                telefone=row[3]
            ))
        return medicos
    except sqlite3.Error as e:
        print(f"Erro ao consultar médicos: {e}")
        return []
    finally:
        conexao.close()

def consultar_medico_por_cpf(cpf):
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
        print(f"Erro ao consultar médico por CPF: {e}")
        return None
    finally:
        conexao.close()

def excluir_medico(cpf):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM medicos WHERE cpf_medico = ?", (cpf,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir médico: {e}")
        return False
    finally:
        conexao.close()

def alterar_medico(medico):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            UPDATE medicos 
            SET numero_registro = ?, ano_registro = ?, telefone = ?
            WHERE cpf_medico = ?
        ''', (
            medico.numero_registro,
            medico.ano_registro,
            medico.telefone,
            medico.cpf_medico
        ))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao alterar médico: {e}")
        return False
    finally:
        conexao.close()

def buscar_medicos_por_registro(numero_registro):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM medicos WHERE numero_registro LIKE ?", (f'%{numero_registro}%',))
        resultados = cursor.fetchall()
        medicos = []
        for row in resultados:
            medicos.append(Medicos(
                cpf_medico=row[0],
                numero_registro=row[1],
                ano_registro=row[2],
                telefone=row[3]
            ))
        return medicos
    except sqlite3.Error as e:
        print(f"Erro ao buscar médicos por registro: {e}")
        return []
    finally:
        conexao.close()

def consultar_medicos_com_departamento():
    """Consulta médicos com informações de departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                m.cpf_medico,
                m.numero_registro,
                m.ano_registro,
                m.telefone,
                f.nome,
                f.cargo,
                d.nome as nome_departamento
            FROM medicos m
            LEFT JOIN funcionarios_hospital f ON m.cpf_medico = f.cpf
            LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
            ORDER BY f.nome
        ''')
        
        resultados = cursor.fetchall()
        medicos = []
        for row in resultados:
            medicos.append({
                'cpf_medico': row[0],
                'numero_registro': row[1],
                'ano_registro': row[2],
                'telefone': row[3],
                'nome': row[4],
                'cargo': row[5],
                'nome_departamento': row[6]
            })
        return medicos
    except sqlite3.Error as e:
        print(f"Erro ao consultar médicos com departamentos: {e}")
        return []
    finally:
        conexao.close()

def consultar_medicos_com_departamento_e_obitos():
    """Consulta médicos com departamento e contagem de óbitos"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                m.cpf_medico,
                m.numero_registro,
                m.ano_registro,
                m.telefone,
                f.nome,
                f.cargo,
                d.nome as nome_departamento,
                COALESCE((
                    SELECT COUNT(*) 
                    FROM obitos o 
                    WHERE o.id_medico = m.cpf_medico
                ), 0) as total_obitos
            FROM medicos m
            LEFT JOIN funcionarios_hospital f ON m.cpf_medico = f.cpf
            LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
            ORDER BY f.nome
        ''')
        
        resultados = cursor.fetchall()
        medicos = []
        for row in resultados:
            medicos.append({
                'cpf_medico': row[0],
                'numero_registro': row[1],
                'ano_registro': row[2],
                'telefone': row[3],
                'nome': row[4],
                'cargo': row[5],
                'nome_departamento': row[6],
                'total_obitos': row[7]
            })
        return medicos
    except sqlite3.Error as e:
        print(f"Erro ao consultar médicos com departamentos e óbitos: {e}")
        return []
    finally:
        conexao.close()

def consultar_medicos_com_departamento_e_obitos():
    """Consulta médicos com departamento e contagem de óbitos"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                m.cpf_medico,
                m.numero_registro,
                m.ano_registro,
                m.telefone,
                f.nome,
                f.cargo,
                d.nome as nome_departamento,
                COALESCE((
                    SELECT COUNT(*) 
                    FROM obitos o 
                    WHERE o.id_medico = m.cpf_medico
                ), 0) as total_obitos
            FROM medicos m
            LEFT JOIN funcionarios_hospital f ON m.cpf_medico = f.cpf
            LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
            ORDER BY f.nome
        ''')
        
        resultados = cursor.fetchall()
        medicos = []
        for row in resultados:
            medicos.append({
                'cpf_medico': row[0],
                'numero_registro': row[1],
                'ano_registro': row[2],
                'telefone': row[3],
                'nome': row[4],
                'cargo': row[5],
                'nome_departamento': row[6],
                'total_obitos': row[7]
            })
        return medicos
    except sqlite3.Error as e:
        print(f"Erro ao consultar médicos com departamentos e óbitos: {e}")
        return []
    finally:
        conexao.close()