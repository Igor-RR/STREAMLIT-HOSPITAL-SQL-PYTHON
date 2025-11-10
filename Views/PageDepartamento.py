import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
from Models.Departamentos import Departamentos
import Controllers.DepartamentosController as DepartamentosController

def show_departamentos_page():
    st.title('Cadastro de Departamentos')
    
    # Menu de operações para Departamentos
    Page_Departamentos = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Departamentos == "Incluir":
        st.subheader("Incluir Novo Departamento")
        
        with st.form(key="incluir_departamento"):
            nome = st.text_input("Nome do Departamento:")
            numero_funcionarios = st.number_input("Número de Funcionários:", min_value=0, step=1)
            
            if st.form_submit_button("Inserir Departamento"):
                if nome.strip():
                    novo_departamento = Departamentos(
                        id=None,
                        nome=nome.strip(),
                        numero_funcionarios=numero_funcionarios
                    )
                    
                    if DepartamentosController.incluir_departamento(novo_departamento):
                        st.toast("✅ Departamento cadastrado com sucesso!", icon="✅")
                        st.rerun()
                    else:
                        st.toast("❌ Erro ao cadastrar departamento!", icon="❌")
                else:
                    st.toast("⚠️ Por favor, informe o nome do departamento!", icon="⚠️")

    elif Page_Departamentos == "Consultar":
        st.subheader("Consultar Departamentos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Consultar Todos"):
                departamentos = DepartamentosController.consultar_departamentos()
                if departamentos:
                    # Converter para DataFrame
                    dados = []
                    for depto in departamentos:
                        dados.append({
                            "ID": depto.id,
                            "Nome": depto.nome,
                            "Nº Funcionários": depto.numero_funcionarios
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas
                    st.subheader("Estatísticas")
                    total_funcionarios = df["Nº Funcionários"].sum()
                    total_departamentos = len(df)
                    media_funcionarios = total_funcionarios / total_departamentos if total_departamentos > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Departamentos", total_departamentos)
                    with col2:
                        st.metric("Total Funcionários", total_funcionarios)
                    with col3:
                        st.metric("Média por Depto", f"{media_funcionarios:.1f}")
                else:
                    st.info("Nenhum departamento cadastrado.")
        
        with col2:
            st.subheader("Buscar por Nome")
            nome_busca = st.text_input("Digite o nome:")
            if st.button("Buscar"):
                if nome_busca.strip():
                    departamentos = DepartamentosController.buscar_departamentos_por_nome(nome_busca.strip())
                    if departamentos:
                        dados = []
                        for depto in departamentos:
                            dados.append({
                                "ID": depto.id,
                                "Nome": depto.nome,
                                "Nº Funcionários": depto.numero_funcionarios
                            })
                        st.dataframe(pd.DataFrame(dados), use_container_width=True)
                        st.toast(f"✅ Encontrados {len(departamentos)} departamentos!", icon="✅")
                    else:
                        st.info("Nenhum departamento encontrado com esse nome.")
                        st.toast("🔍 Nenhum departamento encontrado!", icon="🔍")
                else:
                    st.toast("⚠️ Digite um nome para buscar!", icon="⚠️")

    elif Page_Departamentos == "Excluir":
        st.subheader("Excluir Departamento")
        
        departamentos = DepartamentosController.consultar_departamentos()
        if departamentos:
            # Converter para DataFrame
            dados = []
            for depto in departamentos:
                dados.append({
                    "ID": depto.id,
                    "Nome": depto.nome,
                    "Nº Funcionários": depto.numero_funcionarios
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do departamento para excluir
            ids_departamentos = [depto.id for depto in departamentos]
            nomes_departamentos = [f"{depto.id} - {depto.nome}" for depto in departamentos]
            
            departamento_selecionado = st.selectbox(
                "Selecione o departamento para excluir:",
                options=nomes_departamentos,
                index=0
            )
            
            # Extrair ID do departamento selecionado
            id_excluir = int(departamento_selecionado.split(" - ")[0])
            
            # Mostrar informações do departamento selecionado
            depto_info = next((depto for depto in departamentos if depto.id == id_excluir), None)
            if depto_info:
                st.warning(f"⚠️ **Departamento selecionado para exclusão:**")
                st.write(f"**ID:** {depto_info.id}")
                st.write(f"**Nome:** {depto_info.nome}")
                st.write(f"**Nº de Funcionários:** {depto_info.numero_funcionarios}")
            
            if st.button("Excluir Departamento", type="primary"):
                if DepartamentosController.excluir_departamento(id_excluir):
                    st.toast("✅ Departamento excluído com sucesso!", icon="✅")
                    st.rerun()
                else:
                    st.toast("❌ Erro ao excluir departamento!", icon="❌")
        else:
            st.info("Nenhum departamento cadastrado.")
            st.toast("📝 Nenhum departamento para excluir!", icon="📝")

    elif Page_Departamentos == "Alterar":
        st.subheader("Alterar Departamento")
        
        departamentos = DepartamentosController.consultar_departamentos()
        if departamentos:
            # Converter para DataFrame
            dados = []
            for depto in departamentos:
                dados.append({
                    "ID": depto.id,
                    "Nome": depto.nome,
                    "Nº Funcionários": depto.numero_funcionarios
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Seleção do departamento para alterar
            nomes_departamentos = [f"{depto.id} - {depto.nome}" for depto in departamentos]
            
            departamento_selecionado = st.selectbox(
                "Selecione o departamento para alterar:",
                options=nomes_departamentos,
                key="alterar_select"
            )
            
            # Extrair ID do departamento selecionado
            id_alterar = int(departamento_selecionado.split(" - ")[0])
            
            # Buscar dados do departamento selecionado
            depto_original = DepartamentosController.consultar_departamento_por_id(id_alterar)
            
            if depto_original:
                with st.form(key="alterar_departamento"):
                    st.write("### Editar Departamento")
                    
                    nome = st.text_input("Nome do Departamento:", value=depto_original.nome)
                    numero_funcionarios = st.number_input(
                        "Número de Funcionários:", 
                        min_value=0, 
                        step=1,
                        value=depto_original.numero_funcionarios
                    )
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        if nome.strip():
                            departamento_atualizado = Departamentos(
                                id=depto_original.id,
                                nome=nome.strip(),
                                numero_funcionarios=numero_funcionarios
                            )
                            
                            if DepartamentosController.alterar_departamento(departamento_atualizado):
                                st.toast("✅ Departamento alterado com sucesso!", icon="✅")
                                st.rerun()
                            else:
                                st.toast("❌ Erro ao alterar departamento!", icon="❌")
                        else:
                            st.toast("⚠️ Por favor, informe o nome do departamento!", icon="⚠️")
        else:
            st.info("Nenhum departamento cadastrado.")
            st.toast("📝 Nenhum departamento para alterar!", icon="📝")

# Para testar a página individualmente
if __name__ == "__main__":
    show_departamentos_page()