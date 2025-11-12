import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Obitos import Obitos
import Controllers.ObitosController as ObitosController

def show_obitos_page():
    st.title('Cadastro de Óbitos 💀')
    
    Page_Obitos = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Obitos == "Incluir":
        st.subheader("Incluir Novo Óbito")
        
        with st.form(key="incluir_obito"):
            id_paciente = st.number_input("ID do Paciente:", min_value=1, step=1)
            id_medico = st.number_input("CPF do Médico (use o CPF cadastrado na seção Funcionários):", min_value=1, step=1)  # NOVO CAMPO
            data_obito = st.text_input("Data do Óbito (YYYY-MM-DD):")
            causa_obito = st.text_input("Causa do Óbito:")
            observacoes = st.text_area("Observações:")
            
            if st.form_submit_button("Inserir Óbito"):
                if id_paciente and id_medico and data_obito.strip() and causa_obito.strip():
                    novo_obito = Obitos(
                        id_obito=None,
                        id_paciente=id_paciente,
                        id_medico=id_medico,  # NOVO CAMPO
                        data_obito=data_obito.strip(),
                        causa_obito=causa_obito.strip(),
                        observacoes=observacoes.strip()
                    )
                    
                    if ObitosController.incluir_obito(novo_obito):
                        st.success("Óbito cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar óbito!")
                else:
                    st.warning("Por favor, informe ID do paciente, ID do médico, data e causa do óbito!")

    elif Page_Obitos == "Consultar":
        st.subheader("Consultar Óbitos")
        
        if st.button("Consultar Todos"):
            obitos = ObitosController.consultar_obitos()
            if obitos:
                dados = []
                for obito in obitos:
                    dados.append({
                        "ID Óbito": obito.id_obito,
                        "ID Paciente": obito.id_paciente,
                        "CPF Médico": obito.id_medico,  # NOVO CAMPO (CPF do médico)
                        "Data Óbito": obito.data_obito,
                        "Causa": obito.causa_obito,
                        "Observações": obito.observacoes
                    })
                
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum óbito cadastrado.")

    elif Page_Obitos == "Excluir":
        st.subheader("Excluir Óbito")
        
        obitos = ObitosController.consultar_obitos()
        if obitos:
            dados = []
            for obito in obitos:
                dados.append({
                    "ID Óbito": obito.id_obito,
                    "ID Paciente": obito.id_paciente,
                    "CPF Médico": obito.id_medico,  # NOVO CAMPO (CPF do médico)
                    "Data Óbito": obito.data_obito,
                    "Causa": obito.causa_obito
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            id_excluir = st.number_input("ID do Óbito para excluir:", min_value=1, step=1)
            
            if st.button("Excluir Óbito"):
                if ObitosController.excluir_obito(id_excluir):
                    st.success("Óbito excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir óbito!")
        else:
            st.info("Nenhum óbito cadastrado.")

    elif Page_Obitos == "Alterar":
        st.subheader("Alterar Óbito")
        
        obitos = ObitosController.consultar_obitos()
        if obitos:
            dados = []
            for obito in obitos:
                dados.append({
                    "ID Óbito": obito.id_obito,
                    "ID Paciente": obito.id_paciente,
                    "ID Médico": obito.id_medico,  # NOVO CAMPO
                    "Data Óbito": obito.data_obito,
                    "Causa": obito.causa_obito
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            id_alterar = st.number_input("ID do Óbito para alterar:", min_value=1, step=1)
            
            obito_original = ObitosController.consultar_obito_por_id(id_alterar)
            
            if obito_original:
                with st.form(key="alterar_obito"):
                    st.write("Editar Óbito")
                    
                    id_paciente = st.number_input("ID do Paciente:", value=obito_original.id_paciente)
                    id_medico = st.number_input("CPF do Médico (use o CPF cadastrado na seção Funcionários):", value=obito_original.id_medico)  # NOVO CAMPO
                    data_obito = st.text_input("Data do Óbito:", value=obito_original.data_obito)
                    causa_obito = st.text_input("Causa do Óbito:", value=obito_original.causa_obito)
                    observacoes = st.text_area("Observações:", value=obito_original.observacoes or "")
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        if id_paciente and id_medico and data_obito.strip() and causa_obito.strip():
                            obito_atualizado = Obitos(
                                id_obito=obito_original.id_obito,
                                id_paciente=id_paciente,
                                id_medico=id_medico,  # NOVO CAMPO
                                data_obito=data_obito.strip(),
                                causa_obito=causa_obito.strip(),
                                observacoes=observacoes.strip()
                            )
                            
                            if ObitosController.alterar_obito(obito_atualizado):
                                st.success("Óbito alterado com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao alterar óbito!")
                        else:
                            st.warning("Por favor, informe ID do paciente, ID do médico, data e causa do óbito!")
        else:
            st.info("Nenhum óbito cadastrado.")

if __name__ == "__main__":
    show_obitos_page()