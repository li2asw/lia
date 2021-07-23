from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def next_page(n):
    if n == 1:
        url = "https://www.conjugacao.com.br/verbos-populares/"
    else:
        url = f"https://www.conjugacao.com.br/verbos-populares/{n}"

    response = urlopen(url)
    html = response.read()
    return BeautifulSoup(html, "html.parser")


verbos = []
for n in range(1, 51):
    soup = next_page(n)
    for node in soup.findAll("li"):
        verbos.append(node.get_text())

df = pd.DataFrame(verbos, columns=["verbos_infinito"])
df.to_csv("infinitiveverbs.csv", index=False)
