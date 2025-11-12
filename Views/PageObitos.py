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
        medicos_disponiveis = MedicosController.consultar_medicos_com_departamento_e_obitos()
        
        with st.form(key="incluir_obito"):
            col1, col2 = st.columns(2)
            
            with col1:
                id_paciente = st.number_input("ID do Paciente:", min_value=1, step=1, value=1)
                
                # Seleção do médico
                if medicos_disponiveis:
                    opcoes_medicos = {f"{med['cpf_medico']} - {med['nome']} (Óbitos: {med['total_obitos']})": med['cpf_medico'] for med in medicos_disponiveis}
                    medico_selecionado = st.selectbox("Selecione o Médico*:", options=list(opcoes_medicos.keys()))
                    id_medico = opcoes_medicos[medico_selecionado]
                    
                    # Mostrar informações do médico selecionado
                    medico_info = next((med for med in medicos_disponiveis if med['cpf_medico'] == id_medico), None)
                    if medico_info:
                        st.info(f"**Médico selecionado:** {medico_info['nome']} - {medico_info['cargo']}")
                else:
                    st.error("❌ Nenhum médico cadastrado no sistema! Cadastre médicos primeiro.")
                    id_medico = None
                
                data_obito = st.text_input("Data do Óbito (YYYY-MM-DD)*:", placeholder="2024-01-15")
                
            with col2:
                causa_obito = st.text_area("Causa do Óbito*:", placeholder="Descreva a causa do óbito...", height=100)
                observacoes = st.text_area("Observações:", placeholder="Observações adicionais...", height=100)
            
            st.caption("* Campos obrigatórios")
            
            if st.form_submit_button("💾 Registrar Óbito"):
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
                        st.success("✅ Óbito cadastrado com sucesso!")
                        
                        # Atualizar estatísticas
                        medicos_atualizados = MedicosController.consultar_medicos_com_departamento_e_obitos()
                        medico_atual = next((med for med in medicos_atualizados if med['cpf_medico'] == id_medico), None)
                        if medico_atual:
                            st.info(f"📊 Dr. {medico_info['nome']} agora tem {medico_atual['total_obitos']} óbitos registrados")
                        
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar óbito! Verifique os dados.")
                else:
                    st.warning("⚠️ Por favor, preencha todos os campos obrigatórios!")

    elif Page_Obitos == "Consultar":
        st.subheader("Consultar Óbitos")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("📋 Consultar Todos os Óbitos"):
                obitos = ObitosController.consultar_obitos()
                if obitos:
                    # Buscar informações dos médicos para mostrar nomes
                    medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
                    mapa_medicos = {med['cpf_medico']: med['nome'] for med in medicos}
                    
                    dados = []
                    for obito in obitos:
                        nome_medico = mapa_medicos.get(obito.id_medico, f"Médico ID: {obito.id_medico}")
                        dados.append({
                            "ID Óbito": obito.id_obito,
                            "ID Paciente": obito.id_paciente,
                            "Médico": nome_medico,
                            "Data Óbito": obito.data_obito,
                            "Causa": obito.causa_obito,
                            "Observações": obito.observacoes or "Nenhuma"
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("📊 Estatísticas")
                    total_obitos = len(obitos)
                    medicos_envolvidos = len(set(obito.id_medico for obito in obitos))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Óbitos", total_obitos)
                    with col2:
                        st.metric("Médicos Envolvidos", medicos_envolvidos)
                    with col3:
                        st.metric("Último Registro", obitos[-1].id_obito if obitos else 0)
                else:
                    st.info("📭 Nenhum óbito cadastrado.")

    elif Page_Obitos == "Excluir":
        st.subheader("Excluir Óbito")
        
        obitos = ObitosController.consultar_obitos()
        if obitos:
            # Buscar informações dos médicos
            medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
            mapa_medicos = {med['cpf_medico']: med['nome'] for med in medicos}
            
            dados = []
            for obito in obitos:
                nome_medico = mapa_medicos.get(obito.id_medico, f"Médico ID: {obito.id_medico}")
                dados.append({
                    "ID Óbito": obito.id_obito,
                    "ID Paciente": obito.id_paciente,
                    "Médico": nome_medico,
                    "Data Óbito": obito.data_obito,
                    "Causa": obito.causa_obito
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do óbito para excluir
            obitos_opcoes = [f"ID {obito.id_obito} - Paciente {obito.id_paciente} - {obito.data_obito}" for obito in obitos]
            
            obito_selecionado = st.selectbox(
                "Selecione o óbito para excluir:",
                options=obitos_opcoes,
                index=0
            )
            
            # Extrair ID do óbito selecionado
            id_excluir = int(obito_selecionado.split(" ")[1])
            
            # Mostrar informações completas do óbito selecionado
            obito_info = next((obito for obito in obitos if obito.id_obito == id_excluir), None)
            if obito_info:
                nome_medico = mapa_medicos.get(obito_info.id_medico, f"Médico ID: {obito_info.id_medico}")
                
                st.warning(f"⚠️ **Óbito selecionado para exclusão:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID Óbito:** {obito_info.id_obito}")
                    st.write(f"**ID Paciente:** {obito_info.id_paciente}")
                    st.write(f"**Médico:** {nome_medico}")
                with col2:
                    st.write(f"**Data do Óbito:** {obito_info.data_obito}")
                    st.write(f"**Causa:** {obito_info.causa_obito}")
                    if obito_info.observacoes:
                        st.write(f"**Observações:** {obito_info.observacoes}")
            
            if st.button("🗑️ Excluir Óbito", type="primary"):
                if ObitosController.excluir_obito(id_excluir):
                    st.success("✅ Óbito excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao excluir óbito!")
        else:
            st.info("📭 Nenhum óbito cadastrado.")

    elif Page_Obitos == "Alterar":
        st.subheader("Alterar Óbito")
        
        obitos = ObitosController.consultar_obitos()
        if obitos:
            # Buscar informações dos médicos
            medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
            mapa_medicos = {med['cpf_medico']: med['nome'] for med in medicos}
            
            dados = []
            for obito in obitos:
                nome_medico = mapa_medicos.get(obito.id_medico, f"Médico ID: {obito.id_medico}")
                dados.append({
                    "ID Óbito": obito.id_obito,
                    "ID Paciente": obito.id_paciente,
                    "Médico": nome_medico,
                    "Data Óbito": obito.data_obito,
                    "Causa": obito.causa_obito
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do óbito para alterar
            obitos_opcoes = [f"ID {obito.id_obito} - Paciente {obito.id_paciente} - {obito.data_obito}" for obito in obitos]
            
            obito_selecionado = st.selectbox(
                "Selecione o óbito para alterar:",
                options=obitos_opcoes,
                key="alterar_select_obito"
            )
            
            # Extrair ID do óbito selecionado
            id_alterar = int(obito_selecionado.split(" ")[1])
            
            # Buscar dados do óbito selecionado
            obito_original = ObitosController.consultar_obito_por_id(id_alterar)
            
            if obito_original:
                # Buscar médicos para seleção
                medicos_disponiveis = MedicosController.consultar_medicos_com_departamento_e_obitos()
                
                with st.form(key="alterar_obito"):
                    st.write("### Editar Óbito")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        id_paciente = st.number_input("ID do Paciente*:", min_value=1, step=1, value=obito_original.id_paciente)
                        
                        # Seleção do médico
                        if medicos_disponiveis:
                            opcoes_medicos = {f"{med['cpf_medico']} - {med['nome']} (Óbitos: {med['total_obitos']})": med['cpf_medico'] for med in medicos_disponiveis}
                            
                            # Encontrar o médico atual
                            medico_atual_nome = next(
                                (k for k, v in opcoes_medicos.items() if v == obito_original.id_medico),
                                list(opcoes_medicos.keys())[0]
                            )
                            
                            medico_selecionado = st.selectbox(
                                "Médico*:", 
                                options=list(opcoes_medicos.keys()),
                                index=list(opcoes_medicos.keys()).index(medico_atual_nome)
                            )
                            id_medico = opcoes_medicos[medico_selecionado]
                        else:
                            st.error("Nenhum médico cadastrado!")
                            id_medico = obito_original.id_medico
                        
                        data_obito = st.text_input("Data do Óbito*:", value=obito_original.data_obito)
                    
                    with col2:
                        causa_obito = st.text_area("Causa do Óbito*:", value=obito_original.causa_obito, height=100)
                        observacoes = st.text_area("Observações:", value=obito_original.observacoes or "", height=100)
                    
                    st.caption("* Campos obrigatórios")
                    
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
                                    st.success("✅ Óbito alterado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao alterar óbito!")
                            else:
                                st.warning("⚠️ Por favor, preencha todos os campos obrigatórios!")
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar"):
                            st.rerun()
            else:
                st.error("Óbito não encontrado!")
        else:
            st.info("📭 Nenhum óbito cadastrado.")

if __name__ == "__main__":
    show_obitos_page()