# Classe Mere
class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre=titre
        self.auteur=auteur
        self.date=date
        self.url=url
        self.texte=texte
        self.type="Document"

    def afficher(self):
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Date :", self.date)
        print("URL :", self.url)
        print("Texte :", self.texte)
        print("Source :", self.type)

    def __str__(self):       
        return self.titre 

    # Renvoie le type par défaut, redéfini dans les classes filles.
    def getType(self):
        return "Document"


# Classe Fille
class HackerNewsDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_commentaires = nb_commentaires
        self.type = self.getType()

    def get_nb_commentaires(self):
        return self.nb_commentaires

    def set_nb_comentaires(self, nb):
        self.nb_commentaires = nb

    def getType(self):
        return "Hacker News"

    def __str__(self):
        return(
            f"Titre : {self.titre} |"
            f"Auteur : {self.auteur} |"
            f"Commentaires : {self.nb_commentaires}"
        )
    
# Classe Fille
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
        self.type = self.getType()

    def get_nb_commentaires(self):
        return self.co_auteurs

    def set_nb_comentaires(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def getType(self):
        return "Arxiv"

    def __str__(self):
        return(
            f"Titre : {self.titre} |"
            f"Auteur : {self.auteur} |"
            f"Co_auteurs :{','.join(self.co_auteurs)}"
        )


















    