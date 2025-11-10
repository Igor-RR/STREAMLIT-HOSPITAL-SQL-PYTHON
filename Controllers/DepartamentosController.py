# Controllers/DepartamentosController.py
import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Departamentos import Departamentos

def conectaBD():
    return sqlite3.connect("Hospital.db")

def incluir_departamento(departamento):
    """Inclui um novo departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not departamento.nome or not departamento.nome.strip():
            raise ValueError("Nome do departamento é obrigatório")
        
        if departamento.numero_funcionarios < 0:
            raise ValueError("Número de funcionários não pode ser negativo")
        
        # Inserir no banco
        cursor.execute('''
            INSERT INTO departamentos (nome, numero_funcionarios)
            VALUES (?, ?)
        ''', (departamento.nome.strip(), departamento.numero_funcionarios))
        
        conexao.commit()
        return True
    except ValueError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        print(f"❌ Erro no banco: {e}")
        return False
    finally:
        conexao.close()

def consultar_departamentos():
    """Consulta todos os departamentos"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM departamentos")
        departamentos = cursor.fetchall()
        return [Departamentos(id=row[0], nome=row[1], numero_funcionarios=row[2]) for row in departamentos]
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return []
    finally:
        conexao.close()

def consultar_departamento_por_id(id):
    """Consulta departamento por ID"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM departamentos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Departamentos(id=row[0], nome=row[1], numero_funcionarios=row[2])
        return None
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return None
    finally:
        conexao.close()

def excluir_departamento(id):
    """Exclui um departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM departamentos WHERE id = ?", (id,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir: {e}")
        return False
    finally:
        conexao.close()

def alterar_departamento(departamento):
    """Altera um departamento existente"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not departamento.nome or not departamento.nome.strip():
            raise ValueError("Nome do departamento é obrigatório")
        
        if departamento.numero_funcionarios < 0:
            raise ValueError("Número de funcionários não pode ser negativo")
        
        cursor.execute('''
            UPDATE departamentos 
            SET nome = ?, numero_funcionarios = ?
            WHERE id = ?
        ''', (departamento.nome.strip(), departamento.numero_funcionarios, departamento.id))
        
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

def buscar_departamentos_por_nome(nome):
    """Busca departamentos por nome"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM departamentos WHERE nome LIKE ?", (f'%{nome}%',))
        departamentos = cursor.fetchall()
        return [Departamentos(id=row[0], nome=row[1], numero_funcionarios=row[2]) for row in departamentos]
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()