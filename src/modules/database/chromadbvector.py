# flake8: noqa: E501

import os
import chromadb
import logging
from typing import List


def client(path: str = "./data/chromadb") -> chromadb.ClientAPI:
    """ 
    Cliente para ChromaDB 
    
    Args:
        path (str): caminho em disco para o arquivo
        
    Returns:
        hromadb.ClientAPI: RRetorna uma cliente da instancia de ChromaDB.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return chromadb.PersistentClient(path=path)
    except Exception as e:
        logging.error(e)
        return None


def collection(collection_name: str) -> chromadb.Collection:
    """
    Inicia uma coleção do ChromaDB.

    Args:
        collection_name (str): nome da coleçao.
        
    Returns:
        chromadb.Collection: retorna um objeto de coleç do ChromaDB
    """
    return client().get_or_create_collection(name=collection_name)


def result_to_dict(result: chromadb.QueryResult, cut: float = 1.2) -> List[dict]:
    """
    Recebe um objeto do ChromaDB e  transforma numa lista de dicionários

    Args:
        result (chromadb.QueryResult): resultado da consulta no chromaDB.
        cut (float): corte superior para a distancia (proximidade) dos resultados encontrados.

    Returns:
        List[dic]: | dict: { id, distance, keys ...metadata } | retorna uma lista dicionários (cada dicionário é uma documento encontrado)
    """
    
    retrieval_ids = result['ids']
    retrieval_metadatas = result['metadatas']
    retrieval_distances = result['distances']
    retrieval_documents = result['documents']
    
    # obtem um dicionário com as propriedades
    list_docs = []
    for ids, metadatas, distances, documents in zip(retrieval_ids, retrieval_metadatas, retrieval_distances, retrieval_documents):
        for _id, metadata, distance, document in zip(ids, metadatas, distances, documents):
            if distance > cut:
                continue
            
            doc = { "id": _id, "distance": distance, "keys": document.split() } 
            doc.update(metadata)    
            list_docs.append(doc)
        
    # remove documentos com conteúdo repetido
    content_unique = set()
    docs = []
    for d in list_docs:
        if 'content' not in d:
            docs.append(d)
            continue
        
        content = d['content']
        if content not in content_unique:
            docs.append(d)
            content_unique.add(content)    
    
    return docs
