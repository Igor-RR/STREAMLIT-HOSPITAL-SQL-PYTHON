import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Enfermeiros import Enfermeiros
import Controllers.EnfermeirosController as EnfermeirosController
import Controllers.FuncionariosHospitalController as FuncionarioController

def show_enfermeiro_page():
    st.title('Gestão de Enfermeiros')
    st.info("💡 **Atenção:** Para cadastrar novos enfermeiros, use a página de Funcionários")
    
    # Remove a opção "Incluir" do sidebar
    Page_Enfermeiro = st.sidebar.selectbox("Operações", ["Consultar", "Excluir", "Alterar"])

    if Page_Enfermeiro == "Consultar":
        st.subheader("Consultar Enfermeiros")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Consultar Todos com Departamentos"):
                # USA A NOVA FUNÇÃO COM JOIN
                enfermeiros = EnfermeirosController.consultar_enfermeiros_com_departamento()
                if enfermeiros:
                    dados = []
                    for enf in enfermeiros:
                        dados.append({
                            "CPF": enf['cpf_enfermeiro'],
                            "Nome": enf['nome'],
                            "Cargo": enf['cargo'],
                            "Departamento": enf['nome_departamento'] or "Sem departamento",
                            "Nº COREN": enf['numero_coren'],
                            "Ano Registro": enf['ano_registro']
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("Estatísticas")
                    total_enfermeiros = len(df)
                    departamentos_unicos = df['Departamento'].nunique()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Enfermeiros", total_enfermeiros)
                    with col2:
                        st.metric("Departamentos", departamentos_unicos)
                else:
                    st.info("Nenhum enfermeiro cadastrado.")
            
            if st.button("Consultar Apenas Dados de Enfermeiro"):
                # USA FUNÇÃO ORIGINAL (sem join)
                enfermeiros = EnfermeirosController.consultar_enfermeiros()
                if enfermeiros:
                    dados = []
                    for enf in enfermeiros:
                        dados.append({
                            "CPF": enf.cpf_enfermeiro,
                            "Nº COREN": enf.numero_coren,
                            "Ano Registro": enf.ano_registro
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhum enfermeiro cadastrado.")
        
        with col2:
            st.subheader("Buscar por COREN")
            coren_busca = st.text_input("Digite o COREN:")
            if st.button("Buscar"):
                if coren_busca.strip():
                    enfermeiros = EnfermeirosController.buscar_enfermeiros_por_coren(coren_busca.strip())
                    if enfermeiros:
                        dados = []
                        for enf in enfermeiros:
                            dados.append({
                                "CPF": enf.cpf_enfermeiro,
                                "Nº COREN": enf.numero_coren,
                                "Ano Registro": enf.ano_registro
                            })
                        st.dataframe(pd.DataFrame(dados), use_container_width=True)
                        st.success(f"Encontrados {len(enfermeiros)} enfermeiros!")
                    else:
                        st.info("Nenhum enfermeiro encontrado com esse COREN.")
                else:
                    st.warning("Digite um COREN para buscar!")

    elif Page_Enfermeiro == "Excluir":
        st.subheader("Excluir Enfermeiro")
        st.info("💡 **Atenção:** Esta ação excluirá o enfermeiro completamente do sistema")
        
        # USA A NOVA FUNÇÃO COM JOIN PARA MOSTRAR INFORMAÇÕES COMPLETAS
        enfermeiros = EnfermeirosController.consultar_enfermeiros_com_departamento()
        if enfermeiros:
            dados = []
            for enf in enfermeiros:
                dados.append({
                    "CPF": enf['cpf_enfermeiro'],
                    "Nome": enf['nome'],
                    "Departamento": enf['nome_departamento'] or "Sem departamento",
                    "Nº COREN": enf['numero_coren']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do enfermeiro para excluir
            cpfs_enfermeiros = [enf['cpf_enfermeiro'] for enf in enfermeiros]
            nomes_enfermeiros = [f"{enf['cpf_enfermeiro']} - {enf['nome']}" for enf in enfermeiros]
            
            enfermeiro_selecionado = st.selectbox(
                "Selecione o enfermeiro para excluir:",
                options=nomes_enfermeiros,
                index=0
            )
            
            # Extrair CPF do enfermeiro selecionado
            cpf_excluir = int(enfermeiro_selecionado.split(" - ")[0])
            
            # Mostrar informações completas do enfermeiro selecionado
            enf_info = next((enf for enf in enfermeiros if enf['cpf_enfermeiro'] == cpf_excluir), None)
            if enf_info:
                st.warning(f"**Enfermeiro selecionado para exclusão:**")
                st.write(f"**CPF:** {enf_info['cpf_enfermeiro']}")
                st.write(f"**Nome:** {enf_info['nome']}")
                st.write(f"**Cargo:** {enf_info['cargo']}")
                st.write(f"**Departamento:** {enf_info['nome_departamento'] or 'Sem departamento'}")
                st.write(f"**Nº COREN:** {enf_info['numero_coren']}")
                st.write(f"**Ano Registro:** {enf_info['ano_registro']}")
            
            if st.button("Excluir Enfermeiro", type="primary"):
                # ALTERAÇÃO: Usa a exclusão completa do funcionário
                if FuncionarioController.excluir_funcionario_completo(cpf_excluir):
                    st.success("Enfermeiro excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir enfermeiro!")
        else:
            st.info("Nenhum enfermeiro cadastrado.")

    elif Page_Enfermeiro == "Alterar":
        st.subheader("Alterar Dados do Enfermeiro")
        st.info("💡 **Atenção:** Para alterar dados básicos (nome, cargo, departamento), use a página de Funcionários")
        
        # USA A NOVA FUNÇÃO COM JOIN
        enfermeiros = EnfermeirosController.consultar_enfermeiros_com_departamento()
        if enfermeiros:
            dados = []
            for enf in enfermeiros:
                dados.append({
                    "CPF": enf['cpf_enfermeiro'],
                    "Nome": enf['nome'],
                    "Departamento": enf['nome_departamento'] or "Sem departamento",
                    "Nº COREN": enf['numero_coren']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do enfermeiro para alterar
            nomes_enfermeiros = [f"{enf['cpf_enfermeiro']} - {enf['nome']}" for enf in enfermeiros]
            
            enfermeiro_selecionado = st.selectbox(
                "Selecione o enfermeiro para alterar:",
                options=nomes_enfermeiros,
                key="alterar_select_enfermeiro"
            )
            
            # Extrair CPF do enfermeiro selecionado
            cpf_alterar = int(enfermeiro_selecionado.split(" - ")[0])
            
            # Buscar dados do enfermeiro selecionado (usa função original)
            enf_original = EnfermeirosController.consultar_enfermeiro_por_cpf(cpf_alterar)
            
            if enf_original:
                with st.form(key="alterar_enfermeiro"):
                    st.write("### Editar Dados Específicos do Enfermeiro")
                    
                    numero_coren = st.text_input("Número COREN:", value=enf_original.numero_coren)
                    ano_registro = st.text_input("Ano de Registro:", value=enf_original.ano_registro)
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        if numero_coren.strip() and ano_registro.strip():
                            enfermeiro_atualizado = Enfermeiros(
                                cpf_enfermeiro=enf_original.cpf_enfermeiro,
                                numero_coren=numero_coren.strip(),
                                ano_registro=ano_registro.strip()
                            )
                            
                            if EnfermeirosController.alterar_enfermeiro(enfermeiro_atualizado):
                                st.success("Dados do enfermeiro alterados com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao alterar dados do enfermeiro!")
                        else:
                            st.warning("Por favor, informe COREN e ano de registro!")
        else:
            st.info("Nenhum enfermeiro cadastrado.")

if __name__ == "__main__":
    show_enfermeiro_page()