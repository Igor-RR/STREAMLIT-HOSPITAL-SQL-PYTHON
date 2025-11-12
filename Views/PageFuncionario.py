import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Funcionarios_hospital import Funcionario_hospital
import Controllers.FuncionariosHospitalController as FuncionarioController

def show_funcionario_page():
    st.title('Cadastro de Funcionários')
    st.info("🏥 **Sistema exclusivo para Médicos e Enfermeiros**")

    # Menu de operações para Funcionário
    Page_Funcionario = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Funcionario == "Incluir":
        st.subheader("Cadastrar Novo Profissional")
        
        with st.form(key="incluir_funcionario"):
            # Dados básicos do funcionário
            st.write("### Dados Básicos")
            nome = st.text_input("Nome Completo:")
            cargo = st.text_input("Cargo:")
            cpf = st.number_input("CPF:", min_value=0, step=1, format="%d")
            id_departamento = st.number_input("ID do Departamento:", min_value=1, step=1)
            data_admissao = st.text_input("Data de Admissão (YYYY-MM-DD):", placeholder="2024-01-15")
            salario = st.number_input("Salário:", min_value=0.0, step=100.0, format="%.2f")
            
            # Seleção do tipo de profissional - APENAS MÉDICO OU ENFERMEIRO
            st.write("### Tipo de Profissional")
            tipo_funcionario = st.radio(
                "Selecione o tipo de profissional:",
                ["Médico", "Enfermeiro"],
                horizontal=True
            )
            
            # Campos específicos para Médico
            if tipo_funcionario == "Médico":
                st.write("### Dados do CRM")
                numero_registro = st.text_input("Número de Registro do CRM*:")
                ano_registro = st.text_input(
                    "Ano de Registro do CRM (dd-mm-aaaa)*:",
                    placeholder="dd-mm-aaaa",
                    help="Digite no formato dd-mm-aaaa"
                )
                telefone = st.text_input("Telefone:")
            
            # Campos específicos para Enfermeiro
            else:  # Enfermeiro
                st.write("### Dados do COREN")
                numero_coren = st.text_input("Número COREN*:")
                ano_registro = st.text_input(
                    "Ano de Registro do COREN (dd-mm-aaaa)*:",
                    placeholder="dd-mm-aaaa",
                    help="Digite no formato dd-mm-aaaa"
                )
                telefone = ""  # Enfermeiros não têm telefone específico
            
            st.caption("* Campos obrigatórios")
            
            submit_button = st.form_submit_button("Cadastrar Profissional")
            
            if submit_button:
                # Validações básicas
                if not nome.strip():
                    st.error("❌ Nome é obrigatório!")
                    return
                if not cargo.strip():
                    st.error("❌ Cargo é obrigatório!")
                    return
                if not data_admissao.strip():
                    st.error("❌ Data de admissão é obrigatória!")
                    return
                
                # Validações específicas por tipo
                if tipo_funcionario == "Médico":
                    if not numero_registro.strip():
                        st.error("❌ Número de registro do CRM é obrigatório!")
                        return
                    if not ano_registro.strip():
                        st.error("❌ Ano de registro do CRM é obrigatório!")
                        return
                
                else:  # Enfermeiro
                    if not numero_coren.strip():
                        st.error("❌ Número COREN é obrigatório!")
                        return
                    if not ano_registro.strip():
                        st.error("❌ Ano de registro do COREN é obrigatório!")
                        return
                
                # Criar objeto do funcionário - CORREÇÃO: usando campos atualizados
                novo_funcionario = Funcionario_hospital(
                    cpf=cpf,
                    nome=nome.strip(),
                    cargo=cargo.strip(),
                    id_departamento=id_departamento,
                    data_admissao=data_admissao.strip(),
                    salario=salario
                )
                
                # Preparar dados específicos conforme o tipo
                dados_especificos = {}
                if tipo_funcionario == "Médico":
                    dados_especificos = {
                        'numero_registro': numero_registro.strip(),
                        'ano_registro': ano_registro.strip(),
                        'telefone': telefone.strip()
                    }
                else:  # Enfermeiro
                    dados_especificos = {
                        'numero_coren': numero_coren.strip(),
                        'ano_registro': ano_registro.strip()
                    }
                
                # Inserir no banco (sempre com tipo específico)
                try:
                    sucesso = FuncionarioController.incluir_funcionario_com_tipo(
                        novo_funcionario, 
                        tipo_funcionario, 
                        dados_especificos
                    )
                    
                    if sucesso:
                        st.success(f"✅ {tipo_funcionario} cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar profissional!")
                except Exception as e:
                    st.error(f"❌ Erro no sistema: {str(e)}")

    elif Page_Funcionario == "Consultar":
        st.subheader("Consultar Profissionais")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Consultar Todos os Profissionais"):
                funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
                if funcionarios:
                    # Converter para DataFrame
                    dados = []
                    for func in funcionarios:
                        tipo = func['tipo_funcionario']
                        if tipo == 'Médico':
                            info_especifica = f"CRM: {func['numero_registro']} - {func['ano_registro_medico']}"
                            if func['telefone']:
                                info_especifica += f" | Tel: {func['telefone']}"
                        elif tipo == 'Enfermeiro':
                            info_especifica = f"COREN: {func['numero_coren']} - {func['ano_registro_enfermeiro']}"
                        else:
                            info_especifica = "Sem registro específico"
                            
                        dados.append({
                            "CPF": func['cpf'],
                            "Nome": func['nome'],
                            "Cargo": func['cargo'],
                            "ID Departamento": func['id_departamento'],
                            "Data Admissão": func['data_admissao'],
                            "Salário": f"R$ {func['salario']:.2f}" if func['salario'] else "Não informado",
                            "Tipo": tipo,
                            "Registro": info_especifica
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("Estatísticas")
                    total_funcionarios = len(df)
                    tipos_funcionarios = df['Tipo'].value_counts()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total", total_funcionarios)
                    with col2:
                        st.metric("Médicos", tipos_funcionarios.get('Médico', 0))
                    with col3:
                        st.metric("Enfermeiros", tipos_funcionarios.get('Enfermeiro', 0))
                else:
                    st.info("Nenhum profissional cadastrado.")
        
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
                                "CPF": func.cpf,
                                "Nome": func.nome,
                                "Cargo": func.cargo,
                                "ID Departamento": func.id_departamento,
                                "Data Admissão": func.data_admissao,
                                "Salário": f"R$ {func.salario:.2f}" if func.salario else "Não informado"
                            })
                        st.dataframe(pd.DataFrame(dados), use_container_width=True)
                        st.success(f"✅ Encontrados {len(funcionarios)} profissionais!")
                    else:
                        st.info("Nenhum profissional encontrado com esse nome.")
                else:
                    st.warning("⚠️ Digite um nome para buscar!")

    elif Page_Funcionario == "Excluir":
        st.subheader("Excluir Profissional")
        
        funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
        if funcionarios:
            # Converter para DataFrame
            dados = []
            for func in funcionarios:
                dados.append({
                    "CPF": func['cpf'],
                    "Nome": func['nome'],
                    "Cargo": func['cargo'],
                    "ID Departamento": func['id_departamento'],
                    "Tipo": func['tipo_funcionario']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do profissional para excluir
            nomes_funcionarios = [f"{func['cpf']} - {func['nome']} ({func['tipo_funcionario']})" for func in funcionarios]
            
            funcionario_selecionado = st.selectbox(
                "Selecione o profissional para excluir:",
                options=nomes_funcionarios,
                index=0
            )
            
            # Extrair CPF do profissional selecionado
            cpf_excluir = int(funcionario_selecionado.split(" - ")[0])
            
            # Mostrar informações do profissional selecionado
            func_info = next((func for func in funcionarios if func['cpf'] == cpf_excluir), None)
            if func_info:
                st.warning(f"⚠️ **Profissional selecionado para exclusão:**")
                st.write(f"**CPF:** {func_info['cpf']}")
                st.write(f"**Nome:** {func_info['nome']}")
                st.write(f"**Cargo:** {func_info['cargo']}")
                st.write(f"**ID Departamento:** {func_info['id_departamento']}")
                st.write(f"**Data Admissão:** {func_info['data_admissao']}")
                st.write(f"**Salário:** R$ {func_info['salario']:.2f}" if func_info['salario'] else "**Salário:** Não informado")
                st.write(f"**Tipo:** {func_info['tipo_funcionario']}")
                
                # Mostrar informações específicas
                if func_info['tipo_funcionario'] == 'Médico':
                    st.write(f"**CRM:** {func_info['numero_registro']} - {func_info['ano_registro_medico']}")
                    if func_info['telefone']:
                        st.write(f"**Telefone:** {func_info['telefone']}")
                elif func_info['tipo_funcionario'] == 'Enfermeiro':
                    st.write(f"**COREN:** {func_info['numero_coren']} - {func_info['ano_registro_enfermeiro']}")
            
            if st.button("Excluir Profissional", type="primary"):
                if FuncionarioController.excluir_funcionario_completo(cpf_excluir):
                    st.success("✅ Profissional excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao excluir profissional!")
        else:
            st.info("Nenhum profissional cadastrado.")

    elif Page_Funcionario == "Alterar":
        st.subheader("Alterar Dados do Profissional")
        
        funcionarios = FuncionarioController.consultar_funcionarios_com_tipo()
        if funcionarios:
            # Converter para DataFrame
            dados = []
            for func in funcionarios:
                dados.append({
                    "CPF": func['cpf'],
                    "Nome": func['nome'],
                    "Cargo": func['cargo'],
                    "ID Departamento": func['id_departamento'],
                    "Tipo": func['tipo_funcionario']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do profissional para alterar
            nomes_funcionarios = [f"{func['cpf']} - {func['nome']} ({func['tipo_funcionario']})" for func in funcionarios]
            
            funcionario_selecionado = st.selectbox(
                "Selecione o profissional para alterar:",
                options=nomes_funcionarios,
                key="alterar_select_funcionario"
            )
            
            # Extrair CPF do profissional selecionado
            cpf_alterar = int(funcionario_selecionado.split(" - ")[0])
            
            # Buscar dados do profissional selecionado
            func_original = FuncionarioController.consultar_funcionario_por_cpf(cpf_alterar)
            
            if func_original:
                with st.form(key="alterar_funcionario"):
                    st.write("### Editar Dados Básicos")
                    
                    nome = st.text_input("Nome Completo:", value=func_original.nome)
                    cargo = st.text_input("Cargo:", value=func_original.cargo)
                    id_departamento = st.number_input(
                        "ID do Departamento:", 
                        min_value=1, 
                        step=1,
                        value=func_original.id_departamento
                    )
                    data_admissao = st.text_input(
                        "Data de Admissão:", 
                        value=func_original.data_admissao
                    )
                    salario = st.number_input(
                        "Salário:", 
                        min_value=0.0, 
                        step=100.0, 
                        format="%.2f",
                        value=float(func_original.salario) if func_original.salario else 0.0
                    )
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        if nome.strip() and cargo.strip() and data_admissao.strip():
                            funcionario_atualizado = Funcionario_hospital(
                                cpf=func_original.cpf,
                                nome=nome.strip(),
                                cargo=cargo.strip(),
                                id_departamento=id_departamento,
                                data_admissao=data_admissao.strip(),
                                salario=salario
                            )
                            
                            if FuncionarioController.alterar_funcionario(funcionario_atualizado):
                                st.success("✅ Dados básicos alterados com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao alterar dados!")
                        else:
                            st.warning("⚠️ Por favor, informe nome, cargo e data de admissão!")
        else:
            st.info("Nenhum profissional cadastrado.")

if __name__ == "__main__":
    show_funcionario_page()