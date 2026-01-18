import os
import numpy as np
from typing import List, Dict, Any

class RAGEngine:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2", knowledge_dir: str = None):
        # Determine strict absolute path to knowledge_base
        current_file_dir = os.path.dirname(os.path.abspath(__file__)) 
        project_root = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
        self.knowledge_dir = os.path.join(project_root, "knowledge_base")
        self.model_name = model_name
        self._model = None
        self._faiss = None
            
        print(f"--- [DEBATE CORE] RAG SYSTEM STARTUP ---")
        print(f"Targeting Knowledge Base: {self.knowledge_dir}")
        
        self.index = None
        self.chunks = []
        self.chunk_metadata = []
        
        self.index_path = os.path.join(project_root, "backend", "faiss_index.bin")
        self.metadata_path = os.path.join(project_root, "backend", "metadata.pkl")
        
        # Initialize index (will be fast if cache exists)
        self.refresh_index()

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            print(f"Loading Embedding Model ({self.model_name})...")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    @property
    def faiss_lib(self):
        if self._faiss is None:
            import faiss
            self._faiss = faiss
        return self._faiss

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        from pypdf import PdfReader
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

    def read_text_file(self, text_path: str) -> str:
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file {text_path}: {e}")
            return ""

    def _get_kb_state(self):
        """Returns a string representing the state of the knowledge base (filenames only for stability)."""
        if not os.path.exists(self.knowledge_dir):
            return "empty"
        
        # Include ONLY .txt files
        files = [f for f in os.listdir(self.knowledge_dir) if f.endswith('.txt')]
        
        # Using sorted filenames and sizes for a more stable state than mtime on OneDrive
        state = ""
        for f in sorted(files):
            path = os.path.join(self.knowledge_dir, f)
            state += f"{f}_{os.path.getsize(path)}|"
        return state

    def refresh_index(self, force=False):
        """Reloads all TXT files from knowledge_base and rebuilds the FAISS index if needed."""
        import pickle
        
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            return

        current_state = self._get_kb_state()
        
        # Try to load existing index if state hasn't changed
        if not force and os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'rb') as f:
                    saved_data = pickle.load(f)
                
                if saved_data.get("state") == current_state:
                    print("--- RAG: Loading existing index (Instant) ---")
                    self.index = self.faiss_lib.read_index(self.index_path)
                    self.chunks = saved_data["chunks"]
                    self.chunk_metadata = saved_data["chunk_metadata"]
                    return
            except Exception as e:
                print(f"Index rebuild required.")

        # Rebuild Index...
        print("--- RAG: Rebuilding Index ---")
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        # INCREASED CHUNK SIZE TO 1000 for better context
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        
        self.chunks = []
        self.chunk_metadata = []
        
        # Gather all files
        all_files = [f for f in os.listdir(self.knowledge_dir) if f.endswith('.txt')]
        if not all_files:
            return

        all_text_chunks = []
        for file_name in all_files:
            file_path = os.path.join(self.knowledge_dir, file_name)
            print(f"Syncing: {file_name}...")
            
            full_text = self.read_text_file(file_path)
            
            if not full_text.strip(): continue

            file_chunks = text_splitter.split_text(full_text)
            for i, chunk in enumerate(file_chunks):
                all_text_chunks.append(chunk)
                self.chunk_metadata.append({
                    "source": file_name,
                    "chunk_id": i,
                    "content": chunk.lower() # For search optimization
                })

        if not all_text_chunks: return

        print(f"Encoding {len(all_text_chunks)} chunks...")
        embeddings = self.model.encode(all_text_chunks, show_progress_bar=True)
        
        self.index = self.faiss_lib.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
        self.chunks = all_text_chunks

        self.faiss_lib.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump({"state": current_state, "chunks": self.chunks, "chunk_metadata": self.chunk_metadata}, f)
        print(f"--- RAG: Index Persistent ---")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index is None or not self.chunks:
            return []

        # 1. Semantic Search (Wide fetch)
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), 20)
        
        # 2. Hybrid Re-scoring
        # Add technical mappings to help French -> English RAG
        terms_to_boost = {
            "génie": ["engineering", "engineer"],
            "informatique": ["computer", "it", "ai"],
            "civil": ["civil"],
            "upf": ["université", "university", "fès"],
            "frais": ["fees", "tuition", "mad"],
            "prix": ["fees", "tuition"]
        }
        
        query_lower = query.lower()
        query_terms = [t.lower() for t in query.split() if len(t) > 2]
        
        # Add mapped terms to query_terms for boosting
        extra_boost_terms = []
        for key, synonyms in terms_to_boost.items():
            if key in query_lower:
                extra_boost_terms.extend(synonyms)
        
        all_boost_terms = list(set(query_terms + extra_boost_terms))
        
        scored_results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1 or idx >= len(self.chunk_metadata): continue
            
            metadata = self.chunk_metadata[idx]
            content = metadata["content"].lower()
            
            # Distance score
            semantic_score = 1.0 / (1.0 + distances[0][i])
            
            # Keyword BOOST
            match_count = 0
            for term in all_boost_terms:
                if term in content:
                    match_count += 1
            
            # Heavy penalty for the encyclopedia noise if it doesn't match main terms
            is_encyclopedia = "encyclopedia" in metadata["source"].lower()
            if is_encyclopedia and match_count < 1:
                semantic_score *= 0.1 # Collapse score for encyclopedia junk

            final_score = semantic_score + (match_count * 2.0) # Strong boost
            scored_results.append((final_score, metadata))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in scored_results[:top_k]]

# Singleton instance
rag_engine = RAGEngine()
