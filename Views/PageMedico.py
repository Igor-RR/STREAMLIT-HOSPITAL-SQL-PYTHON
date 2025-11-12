import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Medicos import Medicos
import Controllers.MedicosController as MedicosController
import Controllers.FuncionariosHospitalController as FuncionarioController

def show_medico_page():
    st.title('Gestão de Médicos')
    st.info("💡 **Atenção:** Para cadastrar novos médicos, use a página de Funcionários")
    
    Page_Medico = st.sidebar.selectbox("Operações", ["Consultar", "Excluir", "Alterar"])

    if Page_Medico == "Consultar":
        st.subheader("Consultar Médicos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Consultar Todos com Departamentos e Óbitos"):
                # USA A NOVA FUNÇÃO COM JOIN E CONTAGEM DE ÓBITOS
                medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
                if medicos:
                    dados = []
                    for med in medicos:
                        dados.append({
                            "CPF": med['cpf_medico'],
                            "Nome": med['nome'],
                            "Cargo": med['cargo'],
                            "Departamento": med['nome_departamento'] or "Sem departamento",
                            "Nº Registro": med['numero_registro'],
                            "Ano Registro": med['ano_registro'],
                            "Telefone": med['telefone'] or "Não informado",
                            "Óbitos Registrados": med['total_obitos']
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("📊 Estatísticas")
                    total_medicos = len(df)
                    departamentos_unicos = df['Departamento'].nunique()
                    total_obitos = df['Óbitos Registrados'].sum()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Médicos", total_medicos)
                    with col2:
                        st.metric("Departamentos", departamentos_unicos)
                    with col3:
                        st.metric("Total Óbitos", total_obitos)
                        
                    # Médico com mais óbitos
                    if total_obitos > 0:
                        medico_mais_obitos = df.loc[df['Óbitos Registrados'].idxmax()]
                        st.info(f"🏆 **Médico com mais óbitos:** {medico_mais_obitos['Nome']} ({medico_mais_obitos['Óbitos Registrados']} óbitos)")
                else:
                    st.info("Nenhum médico cadastrado.")
            
            if st.button("Consultar Apenas Dados de Médico"):
                medicos = MedicosController.consultar_medicos()
                if medicos:
                    dados = []
                    for med in medicos:
                        dados.append({
                            "CPF": med.cpf_medico,
                            "Nº Registro": med.numero_registro,
                            "Ano Registro": med.ano_registro,
                            "Telefone": med.telefone or "Não informado"
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    st.info(f"📋 Total de {len(medicos)} médico(s) cadastrado(s)")
                else:
                    st.info("Nenhum médico cadastrado na tabela 'medicos'.")
        
        with col2:
            st.subheader("🔍 Buscar por Registro")
            registro_busca = st.text_input("Digite o número de registro:")
            if st.button("Buscar Médico"):
                if registro_busca.strip():
                    medicos = MedicosController.buscar_medicos_por_registro(registro_busca.strip())
                    if medicos:
                        dados = []
                        for med in medicos:
                            dados.append({
                                "CPF": med.cpf_medico,
                                "Nº Registro": med.numero_registro,
                                "Ano Registro": med.ano_registro,
                                "Telefone": med.telefone or "Não informado"
                            })
                        st.dataframe(pd.DataFrame(dados), use_container_width=True)
                        st.success(f"✅ Encontrados {len(medicos)} médico(s)!")
                    else:
                        st.info("❌ Nenhum médico encontrado com esse registro.")
                else:
                    st.warning("⚠️ Digite um registro para buscar!")

    elif Page_Medico == "Excluir":
        st.subheader("Excluir Médico")
        st.info("💡 **Atenção:** Esta ação excluirá o médico completamente do sistema")
        
        medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
        if medicos:
            dados = []
            for med in medicos:
                dados.append({
                    "CPF": med['cpf_medico'],
                    "Nome": med['nome'],
                    "Departamento": med['nome_departamento'] or "Sem departamento",
                    "Nº Registro": med['numero_registro'],
                    "Óbitos": med['total_obitos']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do médico para excluir
            nomes_medicos = [f"{med['cpf_medico']} - {med['nome']} (Óbitos: {med['total_obitos']})" for med in medicos]
            
            medico_selecionado = st.selectbox(
                "Selecione o médico para excluir:",
                options=nomes_medicos,
                index=0
            )
            
            # Extrair CPF do médico selecionado
            cpf_excluir = int(medico_selecionado.split(" - ")[0])
            
            # Mostrar informações completas do médico selecionado
            med_info = next((med for med in medicos if med['cpf_medico'] == cpf_excluir), None)
            if med_info:
                st.warning(f"**Médico selecionado para exclusão:**")
                st.write(f"**CPF:** {med_info['cpf_medico']}")
                st.write(f"**Nome:** {med_info['nome']}")
                st.write(f"**Cargo:** {med_info['cargo']}")
                st.write(f"**Departamento:** {med_info['nome_departamento'] or 'Sem departamento'}")
                st.write(f"**Nº Registro:** {med_info['numero_registro']}")
                st.write(f"**Ano Registro:** {med_info['ano_registro']}")
                st.write(f"**Telefone:** {med_info['telefone'] or 'Não informado'}")
                st.write(f"**Óbitos Registrados:** {med_info['total_obitos']}")
                
                # Aviso especial se o médico tem óbitos registrados
                if med_info['total_obitos'] > 0:
                    st.error("⚠️ **ATENÇÃO:** Este médico tem óbitos registrados! A exclusão pode afetar os registros de óbitos.")
            
            if st.button("🗑️ Excluir Médico", type="primary"):
                if FuncionarioController.excluir_funcionario_completo(cpf_excluir):
                    st.success("✅ Médico excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao excluir médico!")
        else:
            st.info("ℹ️ Nenhum médico cadastrado.")

    elif Page_Medico == "Alterar":
        st.subheader("Alterar Dados do Médico")
        st.info("💡 **Atenção:** Para alterar dados básicos (nome, cargo, departamento), use a página de Funcionários")
        
        medicos = MedicosController.consultar_medicos_com_departamento_e_obitos()
        if medicos:
            dados = []
            for med in medicos:
                dados.append({
                    "CPF": med['cpf_medico'],
                    "Nome": med['nome'],
                    "Departamento": med['nome_departamento'] or "Sem departamento",
                    "Nº Registro": med['numero_registro'],
                    "Óbitos": med['total_obitos']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do médico para alterar
            nomes_medicos = [f"{med['cpf_medico']} - {med['nome']} (Óbitos: {med['total_obitos']})" for med in medicos]
            
            medico_selecionado = st.selectbox(
                "Selecione o médico para alterar:",
                options=nomes_medicos,
                key="alterar_select_medico"
            )
            
            # Extrair CPF do médico selecionado
            cpf_alterar = int(medico_selecionado.split(" - ")[0])
            
            # Buscar dados do médico selecionado
            med_original = MedicosController.consultar_medico_por_cpf(cpf_alterar)
            
            if med_original:
                with st.form(key="alterar_medico"):
                    st.write("### Editar Dados Específicos do Médico")
                    
                    numero_registro = st.text_input("Número de Registro:", value=med_original.numero_registro)
                    
                    ano_registro = st.text_input(
                        "Ano de Registro do CRM:", 
                        value=med_original.ano_registro,
                        help="Digite a data no formato dd-mm-aaaa (ex: 15-03-2023)"
                    )
                    
                    telefone = st.text_input("Telefone:", value=med_original.telefone or "")
                    
                    if st.form_submit_button("💾 Confirmar Alterações"):
                        if numero_registro.strip() and ano_registro.strip():
                            medico_atualizado = Medicos(
                                cpf_medico=med_original.cpf_medico,
                                numero_registro=numero_registro.strip(),
                                ano_registro=ano_registro.strip(),
                                telefone=telefone.strip()
                            )
                            
                            if MedicosController.alterar_medico(medico_atualizado):
                                st.success("✅ Dados do médico alterados com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao alterar dados do médico!")
                        else:
                            st.warning("⚠️ Por favor, informe número e ano de registro!")
        else:
            st.info("ℹ️ Nenhum médico cadastrado.")

if __name__ == "__main__":
    show_medico_page()