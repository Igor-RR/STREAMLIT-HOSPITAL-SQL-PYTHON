import sqlite3

def verificar_funcionarios():
    """Verifica a tabela de funcionários e suas relações"""
    conn = sqlite3.connect('Hospital.db')
    cursor = conn.cursor()
    
    print("🔍 VERIFICANDO FUNCIONÁRIOS E DEPARTAMENTOS...")
    
    # Verifica departamentos
    cursor.execute("SELECT * FROM departamentos")
    departamentos = cursor.fetchall()
    print(f"\n🏥 DEPARTAMENTOS ({len(departamentos)}):")
    for depto in departamentos:
        print(f"  - ID: {depto[0]}, Nome: {depto[1]}, Desc: {depto[2]}")
    
    # Verifica funcionários
    cursor.execute('''
        SELECT f.cpf, f.nome, f.cargo, d.nome, f.data_admissao, f.salario
        FROM funcionarios_hospital f
        LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
    ''')
    funcionarios = cursor.fetchall()
    print(f"\n👥 FUNCIONÁRIOS ({len(funcionarios)}):")
    for func in funcionarios:
        print(f"  - CPF: {func[0]}, Nome: {func[1]}")
        print(f"    Cargo: {func[2]}, Depto: {func[3]}")
        print(f"    Admissão: {func[4]}, Salário: R$ {func[5]}")
    
    # Verifica relação com médicos
    cursor.execute('''
        SELECT f.cpf, f.nome, f.cargo, 
               CASE WHEN m.cpf_medico IS NOT NULL THEN '✅' ELSE '❌' END as eh_medico
        FROM funcionarios_hospital f
        LEFT JOIN medicos m ON f.cpf = m.cpf_medico
        WHERE f.cargo LIKE '%médico%' OR f.cargo LIKE '%Médico%'
    ''')
    medicos_funcionarios = cursor.fetchall()
    print(f"\n👨‍⚕️ FUNCIONÁRIOS MÉDICOS ({len(medicos_funcionarios)}):")
    for med in medicos_funcionarios:
        print(f"  - CPF: {med[0]}, Nome: {med[1]}, Cargo: {med[2]}, Na tabela médicos: {med[3]}")
    
    conn.close()

if __name__ == "__main__":
    verificar_funcionarios()