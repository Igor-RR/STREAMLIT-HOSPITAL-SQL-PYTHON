import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Funcionarios_hospital import Funcionario_hospital
import Controllers.FuncionariosHospitalController as FuncionarioController

def show_funcionario_page():
    st.title('Cadastro de Funcionários')

    # Menu de operações para Funcionário
    Page_Funcionario = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Funcionario == "Incluir":
        st.subheader("Incluir Novo Funcionário")
        
        with st.form(key="incluir_funcionario"):
            # Dados básicos do funcionário
            st.write("### Dados Básicos do Funcionário")
            nome = st.text_input("Nome do Funcionário:")
            cargo = st.text_input("Cargo:")
            cpf = st.number_input("CPF:", min_value=0, step=1, format="%d")
            id_departamento = st.number_input("ID do Departamento:", min_value=1, step=1)
            
            # Seleção do tipo de funcionário
            st.write("### Tipo de Funcionário")
            tipo_funcionario = st.selectbox(
                "Selecione o tipo de funcionário:",
                ["Funcionário Comum", "Médico", "Enfermeiro"]
            )
            
            # Campos específicos para Médico
            if tipo_funcionario == "Médico":
                st.write("### Dados Específicos do Médico")
                numero_registro = st.text_input("Número de Registro do CRM:")
                ano_registro_medico = st.text_input("Ano de Registro do CRM:")
                telefone = st.text_input("Telefone do Médico:")
            
            # Campos específicos para Enfermeiro
            elif tipo_funcionario == "Enfermeiro":
                st.write("### Dados Específicos do Enfermeiro")
                numero_coren = st.text_input("Número COREN:")
                ano_registro_enfermeiro = st.text_input("Ano de Registro do COREN:")
            
            if st.form_submit_button("Inserir Funcionário"):
                if nome.strip() and cargo.strip():
                    novo_funcionario = Funcionario_hospital(
                        nome=nome.strip(),
                        cargo=cargo.strip(),
                        cpf_funcionario=cpf,
                        id_departamento=id_departamento
                    )
                    
                    # Preparar dados específicos conforme o tipo
                    dados_especificos = {}
                    if tipo_funcionario == "Médico":
                        if not numero_registro.strip() or not ano_registro_medico.strip():
                            st.error("❌ Número de registro e ano de registro são obrigatórios para médicos!")
                            return
                        dados_especificos = {
                            'numero_registro': numero_registro,
                            'ano_registro': ano_registro_medico,
                            'telefone': telefone
                        }
                    elif tipo_funcionario == "Enfermeiro":
                        if not numero_coren.strip() or not ano_registro_enfermeiro.strip():
                            st.error("❌ Número COREN e ano de registro são obrigatórios para enfermeiros!")
                            return
                        dados_especificos = {
                            'numero_coren': numero_coren,
                            'ano_registro': ano_registro_enfermeiro
                        }
                    
                    # Usar função apropriada conforme o tipo
                    if tipo_funcionario == "Funcionário Comum":
                        sucesso = FuncionarioController.incluir_funcionario(novo_funcionario)
                    else:
                        sucesso = FuncionarioController.incluir_funcionario_com_tipo(
                            novo_funcionario, 
                            tipo_funcionario, 
                            dados_especificos
                        )
                    
                    if sucesso:
                        st.toast(f"✅ {tipo_funcionario} cadastrado com sucesso!", icon="✅")
                        st.rerun()
                    else:
                        st.toast("❌ Erro ao cadastrar funcionário!", icon="❌")
                else:
                    st.toast("⚠️ Por favor, informe nome e cargo!", icon="⚠️")

    elif Page_Funcionario == "Consultar":
        st.subheader("Consultar Funcionários")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Consultar Todos com Tipo"):
                # Usa a nova função que retorna com tipo
                funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
                if funcionarios:
                    # Converter para DataFrame
                    dados = []
                    for func in funcionarios:
                        tipo = func['tipo_funcionario']
                        if tipo == 'Médico':
                            info_especifica = f"CRM: {func['numero_registro']} - {func['ano_registro_medico']}"
                        elif tipo == 'Enfermeiro':
                            info_especifica = f"COREN: {func['numero_coren']} - {func['ano_registro_enfermeiro']}"
                        else:
                            info_especifica = "Funcionário Comum"
                            
                        dados.append({
                            "CPF": func['cpf_funcionario'],
                            "Nome": func['nome'],
                            "Cargo": func['cargo'],
                            "ID Departamento": func['id_departamento'],
                            "Tipo": tipo,
                            "Informações Específicas": info_especifica
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("Estatísticas")
                    total_funcionarios = len(df)
                    tipos_funcionarios = df['Tipo'].value_counts()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Funcionários", total_funcionarios)
                    with col2:
                        st.metric("Médicos", tipos_funcionarios.get('Médico', 0))
                    with col3:
                        st.metric("Enfermeiros", tipos_funcionarios.get('Enfermeiro', 0))
                else:
                    st.info("Nenhum funcionário cadastrado.")
        
        with col2:
            st.subheader("Buscar por Nome")
            nome_busca = st.text_input("Digite o nome:")
            if st.button("Buscar"):
                if nome_busca.strip():
                    funcionarios = FuncionarioController.buscar_funcionarios_por_nome(nome_busca.strip())
                    if funcionarios:
                        dados = []
                        for func in funcionarios:
                            dados.append({
                                "CPF": func.cpf_funcionario,
                                "Nome": func.nome,
                                "Cargo": func.cargo,
                                "ID Departamento": func.id_departamento
                            })
                        st.dataframe(pd.DataFrame(dados), use_container_width=True)
                        st.toast(f"✅ Encontrados {len(funcionarios)} funcionários!", icon="✅")
                    else:
                        st.info("Nenhum funcionário encontrado com esse nome.")
                        st.toast("🔍 Nenhum funcionário encontrado!", icon="🔍")
                else:
                    st.toast("⚠️ Digite um nome para buscar!", icon="⚠️")

    elif Page_Funcionario == "Excluir":
        st.subheader("Excluir Funcionário")
        
        funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
        if funcionarios:
            # Converter para DataFrame
            dados = []
            for func in funcionarios:
                dados.append({
                    "CPF": func['cpf_funcionario'],
                    "Nome": func['nome'],
                    "Cargo": func['cargo'],
                    "ID Departamento": func['id_departamento'],
                    "Tipo": func['tipo_funcionario']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do funcionário para excluir
            nomes_funcionarios = [f"{func['cpf_funcionario']} - {func['nome']} ({func['tipo_funcionario']})" for func in funcionarios]
            
            funcionario_selecionado = st.selectbox(
                "Selecione o funcionário para excluir:",
                options=nomes_funcionarios,
                index=0
            )
            
            # Extrair CPF do funcionário selecionado
            cpf_excluir = int(funcionario_selecionado.split(" - ")[0])
            
            # Mostrar informações do funcionário selecionado
            func_info = next((func for func in funcionarios if func['cpf_funcionario'] == cpf_excluir), None)
            if func_info:
                st.warning(f"⚠️ **Funcionário selecionado para exclusão:**")
                st.write(f"**CPF:** {func_info['cpf_funcionario']}")
                st.write(f"**Nome:** {func_info['nome']}")
                st.write(f"**Cargo:** {func_info['cargo']}")
                st.write(f"**ID Departamento:** {func_info['id_departamento']}")
                st.write(f"**Tipo:** {func_info['tipo_funcionario']}")
                
                # Mostrar informações específicas
                if func_info['tipo_funcionario'] == 'Médico':
                    st.write(f"**CRM:** {func_info['numero_registro']} - {func_info['ano_registro_medico']}")
                    if func_info['telefone']:
                        st.write(f"**Telefone:** {func_info['telefone']}")
                elif func_info['tipo_funcionario'] == 'Enfermeiro':
                    st.write(f"**COREN:** {func_info['numero_coren']} - {func_info['ano_registro_enfermeiro']}")
            
            if st.button("Excluir Funcionário", type="primary"):
                # Usa a função de exclusão completa
                if FuncionarioController.excluir_funcionario_completo(cpf_excluir):
                    st.toast("✅ Funcionário excluído com sucesso!", icon="✅")
                    st.rerun()
                else:
                    st.toast("❌ Erro ao excluir funcionário!", icon="❌")
        else:
            st.info("Nenhum funcionário cadastrado.")
            st.toast("📝 Nenhum funcionário para excluir!", icon="📝")

    elif Page_Funcionario == "Alterar":
        st.subheader("Alterar Funcionário")
        
        funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
        if funcionarios:
            # Converter para DataFrame
            dados = []
            for func in funcionarios:
                dados.append({
                    "CPF": func['cpf_funcionario'],
                    "Nome": func['nome'],
                    "Cargo": func['cargo'],
                    "ID Departamento": func['id_departamento'],
                    "Tipo": func['tipo_funcionario']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do funcionário para alterar
            nomes_funcionarios = [f"{func['cpf_funcionario']} - {func['nome']} ({func['tipo_funcionario']})" for func in funcionarios]
            
            funcionario_selecionado = st.selectbox(
                "Selecione o funcionário para alterar:",
                options=nomes_funcionarios,
                key="alterar_select_funcionario"
            )
            
            # Extrair CPF do funcionário selecionado
            cpf_alterar = int(funcionario_selecionado.split(" - ")[0])
            
            # Buscar dados do funcionário selecionado
            func_original = FuncionarioController.consultar_funcionario_por_cpf(cpf_alterar)
            
            if func_original:
                with st.form(key="alterar_funcionario"):
                    st.write("### Editar Dados Básicos do Funcionário")
                    
                    nome = st.text_input("Nome do Funcionário:", value=func_original.nome)
                    cargo = st.text_input("Cargo:", value=func_original.cargo)
                    id_departamento = st.number_input(
                        "ID do Departamento:", 
                        min_value=1, 
                        step=1,
                        value=func_original.id_departamento
                    )
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        if nome.strip() and cargo.strip():
                            funcionario_atualizado = Funcionario_hospital(
                                nome=nome.strip(),
                                cargo=cargo.strip(),
                                cpf_funcionario=func_original.cpf_funcionario,
                                id_departamento=id_departamento
                            )
                            
                            if FuncionarioController.alterar_funcionario(funcionario_atualizado):
                                st.toast("✅ Dados básicos do funcionário alterados com sucesso!", icon="✅")
                                st.rerun()
                            else:
                                st.toast("❌ Erro ao alterar funcionário!", icon="❌")
                        else:
                            st.toast("⚠️ Por favor, informe nome e cargo!", icon="⚠️")
        else:
            st.info("Nenhum funcionário cadastrado.")
            st.toast("📝 Nenhum funcionário para alterar!", icon="📝")

if __name__ == "__main__":
    show_funcionario_page()