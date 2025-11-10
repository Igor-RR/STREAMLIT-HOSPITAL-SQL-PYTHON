# Controllers/FuncionarioHospitalController.py
import sqlite3
import sys
import os

# Adiciona o diretório pai ao path para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.Funcionarios_hospital import Funcionario_hospital

def conectaBD():
    return sqlite3.connect("Hospital.db")

def incluir_funcionario(funcionario):
    """Inclui um novo funcionário (apenas dados base)"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not funcionario.nome or not funcionario.nome.strip():
            raise ValueError("Nome do funcionário é obrigatório")
        
        if not funcionario.cargo or not funcionario.cargo.strip():
            raise ValueError("Cargo do funcionário é obrigatório")
        
        if not funcionario.cpf_funcionario:
            raise ValueError("CPF do funcionário é obrigatório")
        
        # Inserir no banco
        cursor.execute('''
            INSERT INTO funcionario_hospital (nome, cargo, cpf_funcionario, id_departamento)
            VALUES (?, ?, ?, ?)
        ''', (
            funcionario.nome.strip(), 
            funcionario.cargo.strip(),
            funcionario.cpf_funcionario,
            funcionario.id_departamento
        ))
        
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

def incluir_funcionario_com_tipo(funcionario, tipo_funcionario, dados_especificos):
    """Inclui um funcionário com seu tipo específico (Médico/Enfermeiro)"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações gerais do funcionário
        if not funcionario.nome or not funcionario.nome.strip():
            raise ValueError("Nome do funcionário é obrigatório")
        
        if not funcionario.cargo or not funcionario.cargo.strip():
            raise ValueError("Cargo do funcionário é obrigatório")
        
        if not funcionario.cpf_funcionario:
            raise ValueError("CPF do funcionário é obrigatório")
        
        # Inserir funcionário base
        cursor.execute('''
            INSERT INTO funcionario_hospital (nome, cargo, cpf_funcionario, id_departamento)
            VALUES (?, ?, ?, ?)
        ''', (
            funcionario.nome.strip(), 
            funcionario.cargo.strip(),
            funcionario.cpf_funcionario,
            funcionario.id_departamento
        ))
        
        # Inserir na tabela específica conforme o tipo
        if tipo_funcionario == "Médico":
            if not dados_especificos.get('numero_registro'):
                raise ValueError("Número de registro do médico é obrigatório")
            if not dados_especificos.get('ano_registro'):
                raise ValueError("Ano de registro do médico é obrigatório")
                
            cursor.execute('''
                INSERT INTO medicos (cpf_medico, numero_registro, ano_registro, telefone)
                VALUES (?, ?, ?, ?)
            ''', (
                funcionario.cpf_funcionario,
                dados_especificos['numero_registro'].strip(),
                dados_especificos['ano_registro'].strip(),
                dados_especificos.get('telefone', '').strip()
            ))
            
        elif tipo_funcionario == "Enfermeiro":
            if not dados_especificos.get('numero_coren'):
                raise ValueError("Número COREN do enfermeiro é obrigatório")
            if not dados_especificos.get('ano_registro'):
                raise ValueError("Ano de registro do enfermeiro é obrigatório")
                
            cursor.execute('''
                INSERT INTO enfermeiros (cpf_enfermeiro, numero_coren, ano_registro)
                VALUES (?, ?, ?)
            ''', (
                funcionario.cpf_funcionario,
                dados_especificos['numero_coren'].strip(),
                dados_especificos['ano_registro'].strip()
            ))
        
        conexao.commit()
        return True
    except ValueError as e:
        conexao.rollback()
        print(f"❌ Erro de validação: {e}")
        return False
    except sqlite3.Error as e:
        conexao.rollback()
        print(f"❌ Erro no banco: {e}")
        return False
    finally:
        conexao.close()

def consultar_funcionarios():
    """Consulta todos os funcionários"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM funcionario_hospital")
        funcionarios = cursor.fetchall()
        return [Funcionario_hospital(
            nome=row[0], 
            cargo=row[1], 
            cpf_funcionario=row[2], 
            id_departamento=row[3]
        ) for row in funcionarios]
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return []
    finally:
        conexao.close()

def consultar_funcionario_por_cpf(cpf):
    """Consulta funcionário por CPF"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM funcionario_hospital WHERE cpf_funcionario = ?", (cpf,))
        row = cursor.fetchone()
        if row:
            return Funcionario_hospital(
                nome=row[0], 
                cargo=row[1], 
                cpf_funcionario=row[2], 
                id_departamento=row[3]
            )
        return None
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar: {e}")
        return None
    finally:
        conexao.close()

def excluir_funcionario(cpf):
    """Exclui um funcionário (apenas da tabela base) - Use excluir_funcionario_completo para exclusão completa"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM funcionario_hospital WHERE cpf_funcionario = ?", (cpf,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir: {e}")
        return False
    finally:
        conexao.close()

def excluir_funcionario_completo(cpf):
    """Exclui um funcionário e seus dados específicos (médico/enfermeiro)"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Verificar se é médico ou enfermeiro para excluir da tabela específica
        cursor.execute("SELECT 1 FROM medicos WHERE cpf_medico = ?", (cpf,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM medicos WHERE cpf_medico = ?", (cpf,))
        
        cursor.execute("SELECT 1 FROM enfermeiros WHERE cpf_enfermeiro = ?", (cpf,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM enfermeiros WHERE cpf_enfermeiro = ?", (cpf,))
        
        # Excluir do funcionário base
        cursor.execute("DELETE FROM funcionario_hospital WHERE cpf_funcionario = ?", (cpf,))
        
        conexao.commit()
        return True
    except sqlite3.Error as e:
        conexao.rollback()
        print(f"❌ Erro ao excluir funcionário completo: {e}")
        return False
    finally:
        conexao.close()

def alterar_funcionario(funcionario):
    """Altera um funcionário existente"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Validações de negócio
        if not funcionario.nome or not funcionario.nome.strip():
            raise ValueError("Nome do funcionário é obrigatório")
        
        if not funcionario.cargo or not funcionario.cargo.strip():
            raise ValueError("Cargo do funcionário é obrigatório")
        
        cursor.execute('''
            UPDATE funcionario_hospital 
            SET nome = ?, cargo = ?, id_departamento = ?
            WHERE cpf_funcionario = ?
        ''', (
            funcionario.nome.strip(), 
            funcionario.cargo.strip(),
            funcionario.id_departamento,
            funcionario.cpf_funcionario
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

def buscar_funcionarios_por_nome(nome):
    """Busca funcionários por nome"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM funcionario_hospital WHERE nome LIKE ?", (f'%{nome}%',))
        funcionarios = cursor.fetchall()
        return [Funcionario_hospital(
            nome=row[0], 
            cargo=row[1], 
            cpf_funcionario=row[2], 
            id_departamento=row[3]
        ) for row in funcionarios]
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()

def buscar_funcionarios_por_departamento(id_departamento):
    """Busca funcionários por departamento"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM funcionario_hospital WHERE id_departamento = ?", (id_departamento,))
        funcionarios = cursor.fetchall()
        return [Funcionario_hospital(
            nome=row[0], 
            cargo=row[1], 
            cpf_funcionario=row[2], 
            id_departamento=row[3]
        ) for row in funcionarios]
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()

def consultar_funcionarios_com_tipo():
    """Consulta todos os funcionários com informações de tipo (Médico/Enfermeiro)"""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT 
                f.cpf_funcionario, f.nome, f.cargo, f.id_departamento,
                CASE 
                    WHEN m.cpf_medico IS NOT NULL THEN 'Médico'
                    WHEN e.cpf_enfermeiro IS NOT NULL THEN 'Enfermeiro'
                    ELSE 'Outro'
                END as tipo_funcionario,
                m.numero_registro, m.ano_registro as ano_registro_medico, m.telefone,
                e.numero_coren, e.ano_registro as ano_registro_enfermeiro
            FROM funcionario_hospital f
            LEFT JOIN medicos m ON f.cpf_funcionario = m.cpf_medico
            LEFT JOIN enfermeiros e ON f.cpf_funcionario = e.cpf_enfermeiro
        ''')
        
        resultados = cursor.fetchall()
        funcionarios_com_tipo = []
        
        for row in resultados:
            funcionario = {
                'cpf_funcionario': row[0],
                'nome': row[1],
                'cargo': row[2],
                'id_departamento': row[3],
                'tipo_funcionario': row[4],
                'numero_registro': row[5],
                'ano_registro_medico': row[6],
                'telefone': row[7],
                'numero_coren': row[8],
                'ano_registro_enfermeiro': row[9]
            }
            funcionarios_com_tipo.append(funcionario)
        
        return funcionarios_com_tipo
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar funcionários com tipo: {e}")
        return []
    finally:
        conexao.close()