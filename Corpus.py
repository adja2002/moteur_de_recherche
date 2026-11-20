from Author import Author
from Document import Document
import pandas as pd

class Corpus:
    def __init__(self,nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add_document(self, doc):
        id_doc = self.ndoc

        # Ajouter le document au dictionnaire
        self.id2doc[id_doc] = doc

        # Vérifier si l'auteur existe déja
        if doc.auteur not in self.authors:
            self.authors[doc.auteur] =  Author(doc.auteur)

        # Ajouter le document a la production de l'auteur
        self.authors[doc.auteur].add(id_doc, doc)

        # Actualiser les compteurs
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

    # Afficher les docs triés par date
    def afficher_par_date(self, n):

        documents = sorted(
            self.id2doc.items(),
            key=lambda item: (
                pd.isna(pd.to_datetime(item[1].date, errors="coerce")),
                pd.to_datetime(item[1].date, errors="coerce")
                if not pd.isna(pd.to_datetime(item[1].date, errors="coerce"))
                else pd.Timestamp.max
            )
        )

        for id_doc, doc in documents[:n]:
            doc.afficher()
            print()

    # Afficher les docs triés par titre
    def afficher_par_titre(self, n):

        documents = sorted(
            self.id2doc.items(),
            key=lambda item: item[1].titre.lower()
        )

        for id_doc, doc in documents[:n]:
            doc.afficher()
            print()

    # Représentation du corpus
    def __repr__(self):
        return (
            f"Corpus : {self.nom}\n"
            f"Nombre de documents : {self.ndoc}\n"
            f"Nombre d'auteurs : {self.naut}"
        )

    # Sauvegarder le corpus
    def save(self, chemin):

        donnees = []

        for id_doc, doc in self.id2doc.items():

            donnees.append({
                "id": id_doc,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte
            })

        df = pd.DataFrame(donnees)

        df.to_csv(chemin, sep="\t", index=False)

        print("Corpus sauvegardé.")

    # Charger un corpus
    @classmethod
    def load(cls, chemin):

        df = pd.read_csv(chemin, sep="\t")

        corpus = cls("Corpus chargé")

        for _, ligne in df.iterrows():

            doc = Document(
                ligne["titre"],
                ligne["auteur"],
                ligne["date"],
                ligne["url"],
                ligne["texte"]
            )

            corpus.add_document(doc)

        return corpus