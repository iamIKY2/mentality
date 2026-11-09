from app.services.ai_guardrails import sanitize_document_text
import os
import pathlib
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional

# Path to persistent ChromaDB database on disk
CHROMA_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
os.makedirs(CHROMA_DATA_DIR, exist_ok=True)

# Persistent Chroma Client
_chroma_client = chromadb.PersistentClient(
    path=CHROMA_DATA_DIR,
    settings=ChromaSettings(anonymized_telemetry=False)
)
_collection = _chroma_client.get_or_create_collection(
    name="enigma_handbook",
    metadata={"hnsw:space": "cosine"}  # Cosine Similarity Metric
)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Sliding Window Chunking with overlap for text processing."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end >= len(text):
            break
        start += (chunk_size - overlap)
    return [c for c in chunks if c]


class VectorStoreService:
    @staticmethod
    def add_or_update_article(article_id: str, title: str, content: str, category: str):
        """Index an article into ChromaDB HNSW collection with instruction-sanitizing."""
        # Sanitize instruction-like patterns to prevent indirect prompt injection
        clean_content = sanitize_document_text(content)
        clean_title = sanitize_document_text(title)
        clean_category = sanitize_document_text(category)

        raw_chunks = chunk_text(clean_content, chunk_size=500, overlap=100)
        if not raw_chunks:
            raw_chunks = [clean_content or clean_title]

        chunks = [f"{clean_title}\n{c}" for c in raw_chunks]

        ids = [f"{article_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "article_id": str(article_id),
                "title": clean_title,
                "category": clean_category,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]

        _collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

    @staticmethod
    def search_similar_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Cosine Similarity HNSW Vector Search in ChromaDB.
        Returns top_k matching document chunks with similarity score and metadata.
        """
        results = _collection.query(
            query_texts=[query],
            n_results=top_k
        )

        output = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metadatas = results["metadatas"][0] if results.get("metadatas") else []
            distances = results["distances"][0] if results.get("distances") else []

            for i in range(len(docs)):
                dist = distances[i] if i < len(distances) else 0.5
                # In Cosine distance, similarity = 1 - distance
                similarity = max(0.0, 1.0 - dist)
                output.append({
                    "chunk": docs[i],
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "similarity": round(similarity, 4),
                })

        return output

    @staticmethod
    def seed_initial_handbook_data(force: bool = False):
        """Seed initial handbook articles into ChromaDB."""
        from app.core.handbook_data import HANDBOOK_ARTICLES

        try:
            if not force and _collection.count() >= len(HANDBOOK_ARTICLES) * 2:
                print(f"[OK] ChromaDB da san sang ({_collection.count()} chunks handbook).")
                return
        except Exception as e:
            print(f"[WARN] Kiem tra ChromaDB: {e}")

        for item in HANDBOOK_ARTICLES:
            VectorStoreService.add_or_update_article(
                article_id=item["id"],
                title=item["title"],
                content=item["content"],
                category=item["category"]
            )
        print(f"[OK] ChromaDB seeded successfully with {len(HANDBOOK_ARTICLES)} handbook articles ({_collection.count()} chunks)!")

    @staticmethod
    async def sync_all_published_articles_from_db(db) -> int:
        """
        Re-index ALL published handbook articles from PostgreSQL into ChromaDB.
        Ensures that ephemeral storage restarts (like deploys on Render) do not lose
        articles created or edited via the admin dashboard.
        """
        from sqlalchemy import select
        from app.db.models.handbook_article import HandbookArticle, ArticleStatus

        stmt = select(HandbookArticle).where(HandbookArticle.status == ArticleStatus.published)
        res = await db.execute(stmt)
        articles = res.scalars().all()
        for art in articles:
            VectorStoreService.add_or_update_article(
                article_id=str(art.id),
                title=art.title,
                content=art.content,
                category=art.category
            )
        return len(articles)
