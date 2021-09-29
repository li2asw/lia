import base64

import pandas as pd
import spacy
import streamlit as st
from annotated_text import annotated_text
from spacy import displacy

from rules.BadWordsRule import BadWordsRule
from rules.MeaninglessDetRule import MeaninglessDetRule
from rules.ThatWhoRule import ThatWhoRule
from rules.ThisGroupRule import ThisGroupRule

rules = [BadWordsRule, ThisGroupRule, MeaninglessDetRule, ThatWhoRule]


def app():
    @st.experimental_memo
    def load_spacy():
        return spacy.load("pt_core_news_lg")

    @st.cache
    def load_nouns():
        return pd.read_csv("4plus_variation_nouns.csv").noun.tolist()

    nlp = load_spacy()
    nouns = load_nouns()

    st.markdown(
        f"""
    <button
        style='
        position:absolut;
        border: 1px solid #D9562B;
        box-sizing:border-box;
        border-radius:12px;
        background: #FF774A;
        width:200px;height:50px;
        left: 100%;
        position: absolute;
        top: -70px;'>
            <a href='https://forms.gle/Nxc2crQk5zXk8SJq7' target="_blank" style = "color:white;">
                Encontrou um erro?
            </a>
    </button>
    """,
        unsafe_allow_html=True,
    )

    st.title("LIA")  # Titulo da pagina
    txt = st.text_area("Escreva seu texto aqui")  # Area para o usuário escrever
    corpus = nlp(txt)  # Processamento do spacy
    response = []  # texto de saida
    transformed_txt = []  # texto transformado

    context = {"badwords": nouns, "response": response, "transformed_txt": transformed_txt}

    # For para analisar cada palavra e popular o texto de saída
    for index, word in enumerate(corpus):
        response.append(word.text + " ")
        transformed_txt.append(word.text)

        before = corpus[index - 1] if index > 0 else word  # Palavra anterior
        after = corpus[index + 1] if index < len(corpus) - 1 else word  # Palavra seguinte

        context["word"] = word
        context["before"] = before
        context["after"] = after
        context["index"] = index

        for rule in rules:
            if rule().check(context):
                rule().refactor(context)

    st.header("Análise Lia")
    annotated_text(*response)
    # st.markdown(" ".join(response))

    st.header("Sugestão de frase:")
    st.markdown(" ".join(transformed_txt))

    with st.expander("Mais detalhes"):
        st.write("""Aqui a gente consegue debugar nossa inabilidade linguística""")
        html = displacy.render(corpus, style="dep")  # svg object
        # Double newlines seem to mess with the rendering
        html = html.replace("\n\n", "\n")
        b64 = base64.b64encode(html.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        st.write(html, unsafe_allow_html=True)
