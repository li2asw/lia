# pip install pysinonimos
# pip install wheel

# https://www.speakingbrazilian.com/post/how-to-identify-the-gender-of-words
# Como regra geral, as palavras terminadas em -A são femininas, e as palavras terminadas em -O são masculinas, mas há muitas palavras com diferentes terminações.
# Palavras terminadas em -OR são masculinas e palavras terminadas em  -ORA são femininas.
# Palavras terminadas em -ANTE, -ENTE e -ISTA não variam e podem ser usadas para os dois gêneros.
# Palavras terminadas em -AGEM, -IDADE e -ÇÃO são femininas.

from unicodedata import normalize
from pysinonimos.sinonimos import Search
import pandas as pd

df = pd.read_csv("4variation_nouns.csv")


def synonyms_for_gender_nouns(palavra):
    # palavra = normalize("NFKD", word).encode("ASCII", "ignore").decode("ASCII").lower()

    if df.loc[df["noun"] == palavra].shape[0] != 0:
        palavra_suporte = df.loc[df["noun"] == palavra].support
        sinonimos = Search(palavra_suporte.values[0]).synonyms()

        substituto = {}
        for i in sinonimos:
            if i.endswith(("ante", "ente", "ista")):
                substituto = i

            if bool(substituto) == True:
                if palavra[-1] == "s":
                    substituto = substituto + "s"
                return substituto
            else:
                return palavra
