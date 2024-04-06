import os

from model import Model
from document import Doc


def run():

    print("\n", "########## Iniciando registro de documentos ##########", "\n")
    path = 'docs/'

    documents_names = os.listdir(path)
    documents_names_size = len(documents_names)
    
    for i, document_name in enumerate(documents_names): 
        
        path_doc = os.path.join(path, document_name)
        doc = Doc(path_doc, document_name)

        print(f"{i+1}/{documents_names_size}: {doc.name} | páginas: {doc.pages} | paragrafos: {doc.paragraphs} | chunks: {doc.chunks} | linhas: {doc.lines}")

        model = Model()
        model.document(doc)
        # embedding.metadata_generation()
        model.generate()
        model.save()
    
    print("\n")
        
if __name__ == "__main__":
    run()