import sys
import os

# Adiciona o diretório pai ao path para importar Models e Controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
import Controllers.PacientesController as PacientesController
import datetime
import time


def _safe_rerun():
    """Tenta forçar rerun do Streamlit de forma compatível com várias versões.

    Primeiro tenta `st.experimental_rerun()`. Se não existir (ou falhar), altera
    um query param com timestamp usando `st.experimental_set_query_params` para
    forçar a atualização da página. Se tudo falhar, apenas informa o usuário.
    """
    try:
        # Versões antigas/normais do Streamlit
        if hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
            return
        # Algumas builds podem expor apenas `rerun` (raro)
        if hasattr(st, 'rerun'):
            st.rerun()
            return
    except Exception:
        pass

    try:
        # Fallback: altera query param para forçar recarregamento
        params = {}
        try:
            params = st.experimental_get_query_params()
        except Exception:
            params = {}
        params["_refresh"] = [str(int(time.time()))]
        try:
            st.experimental_set_query_params(**params)
            return
        except Exception:
            pass
    except Exception:
        pass

    st.info("Atualize a página manualmente para ver as mudanças.")


def _clean_digits(s: str) -> str:
    return ''.join(filter(str.isdigit, s or ""))


def _is_valid_cpf(cpf: str) -> bool:
    """Valida CPF básico (removendo não dígitos). Retorna True se válido."""
    cpf = _clean_digits(cpf)
    if len(cpf) != 11:
        return False
    # Rejeita sequências repetidas (ex: 00000000000)
    if cpf == cpf[0] * 11:
        return False

    def _calc_digit(cpf_slice: str) -> str:
        total = 0
        peso = len(cpf_slice) + 1
        for ch in cpf_slice:
            total += int(ch) * peso
            peso -= 1
        resto = (total * 10) % 11
        return '0' if resto == 10 else str(resto)

    dig1 = _calc_digit(cpf[:9])
    dig2 = _calc_digit(cpf[:9] + dig1)
    return cpf.endswith(dig1 + dig2)


def _format_cpf(cpf: str) -> str:
    s = _clean_digits(str(cpf))
    if len(s) != 11:
        return s
    return f"{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}"

def show_paciente_page():
    st.title('Gestão de Pacientes')

    Page_Paciente = st.sidebar.selectbox("Operações", ["Cadastrar", "Consultar", "Excluir"])

    if Page_Paciente == "Cadastrar":
        st.subheader("Cadastrar Paciente")

        with st.form(key="form_cadastrar_paciente"):
            nome = st.text_input("Nome completo:")
            cpf = st.text_input("CPF (apenas números):")
            data_nasc = st.date_input(
                "Data de nascimento:",
                min_value=datetime.date(1890, 1, 1),
                max_value=datetime.date.today()
            )
            observacoes = st.text_area("Observações:")

            if st.form_submit_button("Cadastrar"):
                if nome.strip() and cpf.strip():
                    # valida CPF numérico simples
                    cpf_num = _clean_digits(cpf)
                    if not cpf_num:
                        st.warning("CPF inválido. Informe apenas números.")
                    else:
                        try:
                            cpf_int = int(cpf_num)
                            data_str = data_nasc.strftime("%Y-%m-%d")
                            ok = PacientesController.inserir_paciente(nome.strip(), cpf_int, data_str, observacoes.strip())
                            if ok:
                                st.success("Paciente cadastrado com sucesso!")
                                _safe_rerun()
                            else:
                                st.error("Erro ao cadastrar paciente. Verifique o log do servidor.")
                        except Exception as e:
                            st.error(f"Erro ao processar dados: {e}")
                else:
                    st.warning("Os campos Nome e CPF são obrigatórios.")

    elif Page_Paciente == "Consultar":
        st.subheader("Consultar Pacientes")
        pacientes = PacientesController.consultar_pacientes()
        if pacientes:
            rows = []
            for p in pacientes:
                id_p, nome_p, cpf_p, data_p, obs_p = p
                cpf_formatado = _format_cpf(cpf_p)
                # formata data para dd/mm/yyyy se possível
                data_formatada = data_p
                try:
                    if data_p:
                        data_dt = datetime.datetime.strptime(data_p, "%Y-%m-%d")
                        data_formatada = data_dt.strftime("%d/%m/%Y")
                except Exception:
                    pass
                rows.append((id_p, nome_p, cpf_formatado, data_formatada, obs_p))

            df = pd.DataFrame(rows, columns=["ID", "Nome", "CPF", "Data Nascimento", "Observações"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum paciente cadastrado.")

    elif Page_Paciente == "Excluir":
        st.subheader("Excluir Paciente")
        pacientes = PacientesController.consultar_pacientes()
        if pacientes:
            opções = [f"{p[0]} - {p[1]} (CPF: {p[2]})" for p in pacientes]
            selecionado = st.selectbox("Selecione o paciente para exclusão:", opções)
            id_sel = int(selecionado.split(" - ")[0])
            if st.button("Excluir Paciente"):
                # marca o paciente para exclusão em session_state para confirmar
                st.session_state['_paciente_para_excluir'] = id_sel

            # Se existe um paciente marcado para exclusão, pede confirmação
            if st.session_state.get('_paciente_para_excluir') == id_sel:
                st.warning(f"Você está prestes a excluir o paciente: {selecionado}. Esta ação é irreversível.")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("Confirmar Exclusão", key="confirm_excluir"):
                        try:
                            if PacientesController.excluir_paciente(id_sel):
                                st.success("Paciente excluído com sucesso!")
                                # limpa o marcador e rerun
                                del st.session_state['_paciente_para_excluir']
                                _safe_rerun()
                            else:
                                st.error("Erro ao excluir paciente.")
                        except Exception as e:
                            st.error(f"Erro ao excluir: {e}")
                with col2:
                    if st.button("Cancelar", key="cancel_excluir"):
                        if '_paciente_para_excluir' in st.session_state:
                            del st.session_state['_paciente_para_excluir']
        else:
            st.info("Nenhum paciente para excluir.")

if __name__ == "__main__":
    show_paciente_page()
