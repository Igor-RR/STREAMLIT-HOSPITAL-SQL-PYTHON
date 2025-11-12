import sqlite3

def verificar_medicos():
    """Verifica se há médicos cadastrados e mostra informações"""
    conn = sqlite3.connect('Hospital.db')
    cursor = conn.cursor()
    
    print("🔍 VERIFICANDO MÉDICOS NO BANCO DE DADOS...")
    
    # Verifica tabela medicos
    cursor.execute("SELECT COUNT(*) FROM medicos")
    total_medicos = cursor.fetchone()[0]
    print(f"📊 Total de médicos na tabela 'medicos': {total_medicos}")
    
    if total_medicos > 0:
        cursor.execute("SELECT * FROM medicos")
        medicos = cursor.fetchall()
        print("\n📋 MÉDICOS CADASTRADOS:")
        for medico in medicos:
            print(f"  - CPF: {medico[0]}, Registro: {medico[1]}, Ano: {medico[2]}, Telefone: {medico[3]}")
    
    # Verifica funcionários que são médicos
    cursor.execute('''
        SELECT f.cpf, f.nome, f.cargo 
        FROM funcionarios_hospital f 
        WHERE f.cargo LIKE '%médico%' OR f.cargo LIKE '%Médico%'
    ''')
    funcionarios_medicos = cursor.fetchall()
    print(f"\n👨‍⚕️ Funcionários com cargo de médico: {len(funcionarios_medicos)}")
    
    for func in funcionarios_medicos:
        print(f"  - CPF: {func[0]}, Nome: {func[1]}, Cargo: {func[2]}")
        
        # Verifica se existe na tabela medicos
        cursor.execute("SELECT COUNT(*) FROM medicos WHERE cpf_medico = ?", (func[0],))
        existe_na_tabela_medicos = cursor.fetchone()[0]
        if existe_na_tabela_medicos == 0:
            print(f"    ⚠️  NÃO está na tabela 'medicos'!")
    
    conn.close()

if __name__ == "__main__":
    verificar_medicos()