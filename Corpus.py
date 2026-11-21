from Author import Author
from Document import Document, HackerNewsDocument, ArxivDocument
import json
import pandas as pd
from DocumentFactory import DocumentFactory

class Corpus:

    # _instance garde l'unique corpus du programme (vide au départ)
    _instance = None

    # Crée le corpus au premier appel, puis renvoie toujours ce même corpus
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise = False
        return cls._instance

          # Remplit le corpus seulement au premier appel, pour ne pas effacer ses documents
    def __init__(self,nom):
      
        if self._initialise:
            return
        self._initialise = True
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

       # Remet le corpus à zéro, pour que load ne charge pas les documents en double (Singleton)
    def vider(self):
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

            # Informations communes
            ligne = {
                "id": id_doc,
                "type": doc.getType(),
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "nb_commentaires": None,
                "co_auteurs": None
            }

            # Informations spécifiques à Hacker News
            if isinstance(doc, HackerNewsDocument):
                ligne["nb_commentaires"] = doc.nb_commentaires

            # Informations spécifiques à Arxiv
            elif isinstance(doc, ArxivDocument):
                ligne["co_auteurs"] = json.dumps(doc.co_auteurs)

            donnees.append(ligne)

        df = pd.DataFrame(donnees)

        df.to_csv(chemin, sep="\t", index=False)

        print("Corpus sauvegardé.")

    # Charger un corpus
    @classmethod
    def load(cls, chemin):

        df = pd.read_csv(chemin, sep="\t")

        corpus = cls("Corpus chargé")
        # Singleton : on vide le corpus existant pour ne pas charger les documents en double
        corpus.vider()

         # Recrée chaque document avec la Factory selon sa colonne "type".
        for _, ligne in df.iterrows():
            nb = ligne["nb_commentaires"]
            co = ligne["co_auteurs"]
            doc = DocumentFactory.creer(
                ligne["type"], ligne["titre"], ligne["auteur"],
                ligne["date"], ligne["url"], ligne["texte"],
                nb_commentaires=0 if pd.isna(nb) else int(nb),
                co_auteurs=[] if pd.isna(co) else json.loads(co)
            )
            corpus.add_document(doc)
                
        return corpus