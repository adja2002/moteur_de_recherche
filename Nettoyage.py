import re

# Motif d'une balise HTML : "<", puis des caractères qui ne sont pas ">", puis ">".
BALISE = re.compile(r"<[^>]+>")

# Motif de la ponctuation : tout caractère qui n'est ni une lettre, ni un chiffre, ni un espace.
PONCTUATION = re.compile(r"[^\w\s]")

# Motif des chiffres : un ou plusieurs chiffres à la suite.
CHIFFRES = re.compile(r"\d+")

# Motif des espaces en trop : plusieurs espaces, tabulations ou retours à la ligne à la suite.
ESPACES = re.compile(r"\s+")


# TD6 2.1 : remplace toutes les balises HTML du texte par des espaces.
def supprimer_balises(texte):
    return BALISE.sub(" ", texte)


# TD6 2.2 : nettoie le texte (balises, minuscules, retours à la ligne, ponctuation, chiffres).
def nettoyer_texte(texte):
    texte = supprimer_balises(texte)
    texte = texte.lower()
    texte = texte.replace("\n", " ")
    texte = PONCTUATION.sub(" ", texte)
    texte = CHIFFRES.sub(" ", texte)
    texte = ESPACES.sub(" ", texte).strip()
    return texte