import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Obitos import Obitos
import Controllers.ObitosController as ObitosController
import Controllers.MedicosController as MedicosController

def show_obitos_page():
    st.title('Cadastro de Óbitos')
    
    Page_Obitos = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Obitos == "Incluir":
        st.subheader("Incluir Novo Óbito")
        
        # Buscar médicos para seleção
        medicos_disponiveis = MedicosController.consultar_medicos_com_departamento()
        
        with st.form(key="incluir_obito"):
            id_paciente = st.number_input("ID do Paciente:", min_value=1, step=1)
            
            # Seleção do médico
            if medicos_disponiveis:
                opcoes_medicos = {f"{med['cpf_medico']} - {med['nome']}": med['cpf_medico'] for med in medicos_disponiveis}
                medico_selecionado = st.selectbox("Selecione o Médico:", options=list(opcoes_medicos.keys()))
                id_medico = opcoes_medicos[medico_selecionado]
            else:
                st.error("Nenhum médico cadastrado no sistema!")
                id_medico = None
            
            data_obito = st.text_input("Data do Óbito (YYYY-MM-DD):", placeholder="2024-01-15")
            causa_obito = st.text_input("Causa do Óbito:", placeholder="Causa do óbito")
            observacoes = st.text_area("Observações:")
            
            if st.form_submit_button("Inserir Óbito"):
                if id_paciente and id_medico and data_obito.strip() and causa_obito.strip():
                    novo_obito = Obitos(
                        id_obito=0,
                        id_paciente=id_paciente,
                        id_medico=id_medico,
                        data_obito=data_obito.strip(),
                        causa_obito=causa_obito.strip(),
                        observacoes=observacoes.strip()
                    )
                    
                    if ObitosController.incluir_obito(novo_obito):
                        st.success("Óbito cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar óbito! Verifique os dados.")
                else:
                    st.warning("Por favor, preencha todos os campos obrigatórios!")

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
                        "ID Médico": obito.id_medico,
                        "Data Óbito": obito.data_obito,
                        "Causa": obito.causa_obito,
                        "Observações": obito.observacoes
                    })
                
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
                
                # Estatísticas
                st.subheader("📊 Estatísticas")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total de Óbitos", len(obitos))
                with col2:
                    st.metric("Último ID", obitos[-1].id_obito)
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
                    "ID Médico": obito.id_medico,
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
                    "ID Médico": obito.id_medico,
                    "Data Óbito": obito.data_obito,
                    "Causa": obito.causa_obito
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            id_alterar = st.number_input("ID do Óbito para alterar:", min_value=1, step=1)
            
            obito_original = ObitosController.consultar_obito_por_id(id_alterar)
            
            if obito_original:
                # Buscar médicos para seleção
                medicos_disponiveis = MedicosController.consultar_medicos_com_departamento()
                
                with st.form(key="alterar_obito"):
                    st.write("Editar Óbito")
                    
                    id_paciente = st.number_input("ID do Paciente:", value=obito_original.id_paciente, min_value=1)
                    
                    # Seleção do médico
                    if medicos_disponiveis:
                        opcoes_medicos = {f"{med['cpf_medico']} - {med['nome']}": med['cpf_medico'] for med in medicos_disponiveis}
                        # Encontrar o médico atual
                        medico_atual = next((k for k, v in opcoes_medicos.items() if v == obito_original.id_medico), list(opcoes_medicos.keys())[0])
                        medico_selecionado = st.selectbox("Médico:", options=list(opcoes_medicos.keys()), index=list(opcoes_medicos.keys()).index(medico_atual))
                        id_medico = opcoes_medicos[medico_selecionado]
                    else:
                        st.error("Nenhum médico cadastrado!")
                        id_medico = obito_original.id_medico
                    
                    data_obito = st.text_input("Data do Óbito:", value=obito_original.data_obito)
                    causa_obito = st.text_input("Causa do Óbito:", value=obito_original.causa_obito)
                    observacoes = st.text_area("Observações:", value=obito_original.observacoes or "")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Salvar Alterações"):
                            if id_paciente and id_medico and data_obito.strip() and causa_obito.strip():
                                obito_atualizado = Obitos(
                                    id_obito=obito_original.id_obito,
                                    id_paciente=id_paciente,
                                    id_medico=id_medico,
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
                                st.warning("Por favor, preencha todos os campos obrigatórios!")
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar"):
                            st.rerun()
            else:
                st.error("Óbito não encontrado!")
        else:
            st.info("Nenhum óbito cadastrado.")

if __name__ == "__main__":
    show_obitos_page()