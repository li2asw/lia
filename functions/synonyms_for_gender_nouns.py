# https://www.speakingbrazilian.com/post/how-to-identify-the-gender-of-words
# Como regra geral, as palavras terminadas em -A são femininas, e as palavras terminadas em -O são masculinas, mas há muitas palavras com diferentes terminações.
# Palavras terminadas em -OR são masculinas e palavras terminadas em  -ORA são femininas.
# Palavras terminadas em -ANTE, -ENTE e -ISTA não variam e podem ser usadas para os dois gêneros.
# Palavras terminadas em -AGEM, -IDADE e -ÇÃO são femininas.

from functions.synonyms import Search
import spacy

def synonyms_for_gender_nouns(df, df_words_freq, word, normalized_word):
    palavra_suporte = df.loc[df["noun"] == normalized_word].support
    sinonimos = Search(palavra_suporte.values[0]).synonyms()

    #exclui sinonimos que não são substantivos
    sinonimos_text = ' '.join(sinonimos)
    nlp = spacy.load("pt_core_news_lg")
    nlp_sinonimos = nlp(sinonimos_text)
    sinonimos_nouns = []
    for token in nlp_sinonimos:
        if token.pos_ == 'NOUN':
            sinonimos_nouns.append(token)

    # pegando sinonimos com score de frequencia maior ou igual a threshold
    df_freq_sinonimos = df_words_freq.query('words in @sinonimos_nouns')
    df_freq_sinonimos = df_freq_sinonimos.query('percentil >= 0.98')
    sinonimos = df_freq_sinonimos['words'].tolist()
    
    # se a palavra não tiver sinônimo, o request retorna 404; se tiver, retorna uma lista
    if isinstance(sinonimos, list):
        substituto_list = []
        for sinonimo in sinonimos:
            if sinonimo.endswith(("ante", "ente", "ista")):
                if normalized_word[-1] == "s":
                    substituto_list.append(sinonimo + "s")
                else:
                    substituto_list.append(sinonimo)

        if len(substituto_list) > 0:
            return ", ".join(substituto_list)
        else:
            return word.text
    else:
        return word.text

