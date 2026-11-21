from Document import Document, HackerNewsDocument, ArxivDocument


# Factory qui crée le bon type de document selon la source.
class DocumentFactory:

    # Renvoie un HackerNewsDocument, un ArxivDocument ou un Document simple selon type_doc.
    @staticmethod
    def creer(type_doc, titre, auteur, date, url, texte, **infos):
        if type_doc == "Hacker News":
            return HackerNewsDocument(titre, auteur, date, url, texte,
                                      infos.get("nb_commentaires", 0))
        elif type_doc == "Arxiv":
            return ArxivDocument(titre, auteur, date, url, texte,
                                 infos.get("co_auteurs", []))
        else:
            return Document(titre, auteur, date, url, texte)