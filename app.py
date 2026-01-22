import streamlit as st
from openai import OpenAI

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Vendas AI", page_icon="💰")

# --- BARRA LATERAL (Para colocar a senha da OpenAI) ---
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("Coloque sua API Key da OpenAI aqui:", type="password")
    st.markdown("[Clique aqui para pegar sua chave na OpenAI](https://platform.openai.com/api-keys)")
    st.warning("Nota: Você precisa de créditos na OpenAI para funcionar.")

# --- TÍTULO E SUBTÍTULO ---
st.title("🛍️ Gerador de Descrições Vendedoras")
st.write("Transforme características simples em textos que vendem muito.")
st.markdown("---")

# --- FORMULÁRIO DE ENTRADA (Onde o usuário digita) ---
col1, col2 = st.columns(2)

with col1:
    produto = st.text_input("Nome do Produto", placeholder="Ex: Tênis Nike Revolution")
    publico = st.text_input("Público Alvo", placeholder="Ex: Corredores iniciantes")

with col2:
    tom_de_voz = st.selectbox(
        "Tom de Voz da Venda",
        ["Persuasivo e Urgente", "Descontraído e Jovem", "Sofisticado e Luxuoso", "Técnico e Profissional"]
    )

caracteristicas = st.text_area("Características do Produto (Lista)", placeholder="Ex: Leve, azul, solado macio, importado...")

# --- O BOTÃO MÁGICO ---
botao_gerar = st.button("✨ Gerar Descrição Agora", type="primary")

# --- A LÓGICA (O Cérebro do App) ---
if botao_gerar:
    if not api_key:
        st.error("Por favor, insira sua API Key na barra lateral esquerda para começar.")
    elif not produto or not caracteristicas:
        st.warning("Preencha o nome do produto e as características.")
    else:
        # Configurando a conexão com a IA
        client = OpenAI(api_key=api_key)
        
        # O Prompt (O comando secreto que enviamos para a IA)
        prompt_sistema = f"""
        Você é um copywriter expert em E-commerce.
        Sua missão é criar uma descrição de produto irresistível para: {produto}.
        Características: {caracteristicas}.
        Público: {publico}.
        Tom de voz: {tom_de_voz}.
        
        Estrutura da resposta:
        1. Um título chamativo (Headline).
        2. Um parágrafo de benefício emocional.
        3. Lista de benefícios (bullets).
        4. Uma chamada para ação (CTA) final.
        Use emojis moderadamente.
        """

        try:
            with st.spinner('A IA está escrevendo seu texto...'):
                resposta = client.chat.completions.create(
                    model="gpt-4o-mini", # Modelo rápido e barato
                    messages=[
                        {"role": "system", "content": "Você é um assistente de vendas."},
                        {"role": "user", "content": prompt_sistema}
                    ]
                )
                
                texto_final = resposta.choices[0].message.content
                
            # --- MOSTRAR O RESULTADO ---
            st.success("Descrição Gerada com Sucesso!")
            st.markdown("### Copie seu texto abaixo:")
            st.code(texto_final, language=None) # Caixa fácil de copiar
            
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Ferramenta criada para acelerar suas vendas.")
