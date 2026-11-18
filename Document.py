class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre=titre
        self.auteur=auteur
        self.date=date
        self.url=url
        self.texte=texte

    def afficher(self):      
        print(f" le titre du document est : {self.titre},l'auteur est:{self.auteur}, la date: {self.date},l'url :{self.url} et le text correspodant est :            {self.texte}")           

    def __str__(self):       
        return f" {self.titre}"

    


















    