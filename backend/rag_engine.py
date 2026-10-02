from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_chunks(chunks, question, top_k=4):

    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        document_vectors = vectorizer.fit_transform(texts)
        question_vector = vectorizer.transform([question])

        similarities = cosine_similarity(
            question_vector,
            document_vectors
        ).flatten()

    except ValueError:
        return chunks[:top_k]

    ranked_indexes = similarities.argsort()[::-1]

    results = []

    for index in ranked_indexes[:top_k]:

        results.append({
            "text": chunks[index]["text"],
            "page": chunks[index]["page"],
            "score": float(similarities[index])
        })

    return results


def create_pdf_context(results):

    context_parts = []

    for result in results:

        context_parts.append(
            f"[Page {result['page']}]\n"
            f"{result['text']}"
        )

    return "\n\n".join(context_parts)