from typing import List

import numpy as np  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore


class SortSortService:
    def __init__(self):
        self.embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")
    def sort_source(self, query: str, search_result: List[dict]):
        try:
            relevant_sources = []
            query_embedding = self.embeddings_model.encode(query)
            for res in search_result:
                res_embedding = self.embeddings_model.encode(res["content"])
                similarity =float( np.dot(query_embedding, res_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(res_embedding)
                    ))
                res["similarity"] = similarity
                if(similarity > 0.5):
                    relevant_sources.append(res)
            return sorted(relevant_sources, key=lambda x: x["similarity"], reverse=True)
        except Exception as e:
            print(e)
            return search_result