import sqlite3

def criar_tabela():
    """Cria a tabela obitos no banco de dados"""
    try:
        conexao = sqlite3.connect("Hospital.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS obitos (
                id_obito INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                data_obito DATE NOT NULL,
                causa_obito TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
            )
        ''')
        
        conexao.commit()

        # Migração: se a coluna id_medico não existir (DBs antigas), adiciona-a.
        cursor.execute("PRAGMA table_info(obitos)")
        cols = [row[1] for row in cursor.fetchall()]
        if 'id_medico' not in cols:
            try:
                cursor.execute("ALTER TABLE obitos ADD COLUMN id_medico INTEGER DEFAULT NULL")
                conexao.commit()
                print("✅ Coluna 'id_medico' adicionada à tabela 'obitos' (migração)")
            except Exception as e:
                print(f"❌ Falha ao adicionar coluna 'id_medico': {e}")

        conexao.close()
        
        print("✅ Tabela 'obitos' criada/verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela obitos: {e}")
        return False

# Executa automaticamente ao importar
criar_tabela()