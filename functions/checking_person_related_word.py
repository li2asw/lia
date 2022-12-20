import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from functions.translate_pt_to_en import translate_pt_to_en

def check_lowest_common_hypernym(row, support_bol=True):
    """
    This function uses wordnet synonyms sets to define a certain word and the method lowest_common_hypernyms to find out
    if the word "person" is the most common "ancestor" word between person itself and the bad word checked. 
    Thus, it is possible to check if a bad word is related to human beings.
    """
    if support_bol:
        word_to_check = row.support
    else: 
        word_to_check = row
    try:
        check = wn.synset('person.n.01') in wn.synset(f'{translate_pt_to_en(word_to_check)}.n.01').lowest_common_hypernyms(wn.synset('person.n.01'))
    except:
        check = 'Lemma não encontrado'
    return check

def main():
    bad_words_df = pd.read_csv("4plus_variation_nouns.csv")
    print(bad_words_df)

    bad_words_df['is_human_related'] = bad_words_df.apply(lambda row: check_lowest_common_hypernym(row), axis=1)
    print(bad_words_df)

    human_related_trues = (bad_words_df.is_human_related == True)
    bad_words_df_true = bad_words_df[human_related_trues]
    print(bad_words_df_true)

    bad_words_df_true.to_csv("4plus_variation_nouns_human_related.csv", index=False)

if __name__ == "__main__":
    main()
