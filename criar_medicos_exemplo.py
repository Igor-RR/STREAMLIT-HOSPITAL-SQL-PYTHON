import sqlite3

def criar_medicos_exemplo():
    """Cria médicos de exemplo para teste"""
    conn = sqlite3.connect('Hospital.db')
    cursor = conn.cursor()
    
    medicos_exemplo = [
        (12345678901, 'CRM-SP12345', '15-03-2020', '(11) 9999-8888'),
        (23456789012, 'CRM-SP67890', '20-07-2019', '(11) 9777-6666'),
        (34567890123, 'CRM-SP54321', '10-11-2021', '(11) 9555-4444')
    ]
    
    try:
        for medico in medicos_exemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO medicos (cpf_medico, numero_registro, ano_registro, telefone)
                VALUES (?, ?, ?, ?)
            ''', medico)
        
        conn.commit()
        print("✅ Médicos de exemplo criados com sucesso!")
        
        # Verifica
        cursor.execute("SELECT COUNT(*) FROM medicos")
        total = cursor.fetchone()[0]
        print(f"📊 Total de médicos no banco: {total}")
        
    except Exception as e:
        print(f"❌ Erro ao criar médicos de exemplo: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_medicos_exemplo()