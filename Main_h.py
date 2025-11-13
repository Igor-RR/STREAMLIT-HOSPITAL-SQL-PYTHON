# main.py
import streamlit as st
import sys
import os

# ========== CONFIGURAÇÃO DE IMPORTAÇÕES ==========
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'Models'))
sys.path.append(os.path.join(current_dir, 'Services'))
sys.path.append(os.path.join(current_dir, 'Controllers'))
sys.path.append(os.path.join(current_dir, 'Views'))

# ========== INICIALIZAÇÃO DO SISTEMA ==========
def inicializar_sistema():
    """Inicializa o banco de dados e verifica todas as dependências"""
    
    # 1. Criar todas as tabelas
    try:
        from Services.tabela_departamento import criar_tabela as criar_departamentos
        from Services.tabela_funcionario_hospital import criar_tabela as criar_funcionarios
        from Services.tabela_medicos import criar_tabela as criar_medicos
        from Services.tabela_enfermeiros import criar_tabela as criar_enfermeiros
        from Services.tabela_obitos import criar_tabela as criar_obitos
        from Services.tabela_pacientes import criar_tabela as criar_pacientes
        
        criar_departamentos()
        criar_funcionarios()
        criar_medicos()
        criar_enfermeiros()
        criar_obitos()
        criar_pacientes()
        
        st.sidebar.success("✅ Banco de dados inicializado!")
    except Exception as e:
        st.sidebar.error(f"❌ Erro no banco: {e}")
        return False
    
    # 2. Verificar se todos os módulos estão importáveis
    try:
        # Verificar Departamentos
        from Models.Departamentos import Departamentos
        from Controllers.DepartamentosController import (
            incluir_departamento, 
            consultar_departamentos,
            excluir_departamento,
            alterar_departamento,
            buscar_departamentos_por_nome,
            consultar_departamento_por_id
        )
        from Views.PageDepartamento import show_departamentos_page

        # Verificar Funcionários
        from Models.Funcionarios_hospital import Funcionario_hospital
        from Controllers.FuncionariosHospitalController import (
            incluir_funcionario,
            consultar_funcionarios,
            excluir_funcionario,
            alterar_funcionario,
            buscar_funcionarios_por_nome,
            consultar_funcionario_por_cpf
        )
        from Views.PageFuncionario import show_funcionario_page

        # Verificar Médicos
        from Models.Medicos import Medicos
        from Controllers.MedicosController import (
            consultar_medicos,
            excluir_medico,
            alterar_medico,
            buscar_medicos_por_registro,
            consultar_medico_por_cpf
        )
        from Views.PageMedico import show_medico_page

        # Verificar Pacientes
        from Models.Paciente import Paciente
        from Controllers.PacientesController import (
            inserir_paciente,
            consultar_pacientes,
            excluir_paciente
        )
        from Views.PagePaciente import show_paciente_page
        from Models.Obitos import Obitos
        import Controllers.ObitosController as ObitosController
        from Views.PageObitos import show_obitos_page

        # Verificar Enfermeiros
        from Models.Enfermeiros import Enfermeiros
        from Controllers.EnfermeirosController import (
            consultar_enfermeiros,
            excluir_enfermeiro,
            alterar_enfermeiro,
            buscar_enfermeiros_por_coren,
            consultar_enfermeiro_por_cpf
        )
        from Views.PageEnfermeiro import show_enfermeiro_page

        # Verificar Óbitos
        from Models.Obitos import Obitos
        import Controllers.ObitosController as ObitosController
        from Views.PageObitos import show_obitos_page
        
        st.sidebar.success("✅ Todos os módulos carregados!")
        return True
        
    except ImportError as e:
        st.sidebar.error(f"❌ Erro de importação: {e}")
        return False

# ========== PÁGINA PRINCIPAL ==========
def main():
    # Configuração da página
    st.set_page_config(
        page_title="Sistema Hospitalar",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar sistema
    if not inicializar_sistema():
        st.error("""
        ⚠️ **Sistema não pode ser inicializado!**
        
        Verifique se todos os arquivos estão no lugar correto.
        """)
        st.stop()
    
    # Menu de navegação
    st.sidebar.title("🏥 Sistema Hospitalar")
    st.sidebar.markdown("---")
    
    pagina = st.sidebar.radio(
        "Navegação",
        ["Departamentos", "Funcionários", "Médicos", "Enfermeiros", "Óbitos", "Pacientes"]
    )
    
    # Navegação entre páginas
    if pagina == "Departamentos":
        from Views.PageDepartamento import show_departamentos_page
        show_departamentos_page()
    elif pagina == "Funcionários":
        from Views.PageFuncionario import show_funcionario_page
        show_funcionario_page()
    elif pagina == "Médicos":
        from Views.PageMedico import show_medico_page
        show_medico_page()
    elif pagina == "Enfermeiros":
        from Views.PageEnfermeiro import show_enfermeiro_page
        show_enfermeiro_page()
    elif pagina == "Óbitos":
        from Views.PageObitos import show_obitos_page
        show_obitos_page()
    elif pagina == "Pacientes":
        from Views.PagePaciente import show_paciente_page
        show_paciente_page()

# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    main()