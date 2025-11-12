import sqlite3

def criar_tabela():
    """Cria a tabela funcionarios_hospital no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        # Primeiro cria a tabela de departamentos se não existir (para a FK)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departamentos (
                id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            )
        ''')
        
        # Agora cria a tabela de funcionários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios_hospital (
                cpf INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                id_departamento INTEGER,
                data_admissao DATE NOT NULL,
                salario DECIMAL(10,2),
                FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
            )
        ''')
        
        # Insere alguns departamentos padrão se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM departamentos")
        if cursor.fetchone()[0] == 0:
            departamentos_padrao = [
                ('Cardiologia', 'Departamento de doenças cardíacas'),
                ('Pediatria', 'Departamento de atendimento infantil'),
                ('Ortopedia', 'Departamento de ossos e articulações'),
                ('Enfermagem', 'Departamento de enfermagem'),
                ('Administração', 'Departamento administrativo')
            ]
            cursor.executemany('INSERT INTO departamentos (nome, descricao) VALUES (?, ?)', departamentos_padrao)
        
        # Insere alguns funcionários de exemplo se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM funcionarios_hospital")
        if cursor.fetchone()[0] == 0:
            funcionarios_exemplo = [
                (12345678901, 'Dr. João Silva', 'Médico Cardiologista', 1, '2020-01-15', 15000.00),
                (23456789012, 'Dra. Maria Santos', 'Médica Pediatra', 2, '2019-03-20', 12000.00),
                (34567890123, 'Dr. Carlos Oliveira', 'Médico Ortopedista', 3, '2021-06-10', 13000.00),
                (45678901234, 'Enf. Ana Costa', 'Enfermeira Chefe', 4, '2018-11-05', 8000.00),
                (56789012345, 'Sr. Roberto Lima', 'Administrador', 5, '2022-02-28', 7000.00)
            ]
            cursor.executemany('''
                INSERT INTO funcionarios_hospital 
                (cpf, nome, cargo, id_departamento, data_admissao, salario) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', funcionarios_exemplo)
        
        conexao.commit()
        conexao.close()
        
        print("✅ Tabela 'funcionarios_hospital' criada/verificada com dados de exemplo!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela funcionarios_hospital: {e}")
        return False

def reiniciar_tabela():
    """Reinicia a tabela funcionarios_hospital (CUIDADO: apaga todos os dados!)"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        # Remove a tabela se existir
        cursor.execute('DROP TABLE IF EXISTS funcionarios_hospital')
        
        # Recria a tabela
        criar_tabela()
        
        conexao.close()
        print("🔄 Tabela 'funcionarios_hospital' reiniciada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao reiniciar tabela funcionarios_hospital: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()