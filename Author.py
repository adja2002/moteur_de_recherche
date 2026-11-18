class Author:
    def __init__(self,name):
        self.name=name
        self.ndoc=0
        self.production={}


    def add(self, identifiant, doc):
        self.production[identifiant]=doc
        self.ndoc +=1


    def __str__(self):
        return f"{self.name} : {self.ndoc} document(s)"