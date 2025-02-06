import re
from dataclasses import asdict, dataclass
from typing import List, Sequence, TypedDict

from pymilvus import MilvusClient


def split_text_into_chunks(  # noqa: C901 WPS231
    text: str,
    limit: int = 200,
) -> Sequence[str]:
    """
    Splits the text into the chunks.

    :param text: text to ensure it's within the limit
    :param limit: max size of the text chunk
    :returns: Sequence/List of strings
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)  # Split by sentence delimiters
    result = []
    buffer = ""

    for sentence in sentences:
        if len(sentence) > limit:
            # Case 3: If a single sentence is bigger than the limit, split it further
            for i in range(0, len(sentence), limit):  # noqa: WPS111
                result.append(sentence[i : i + limit])
        elif len(buffer) + len(sentence) + 1 <= limit:
            # Case 1: If adding this sentence keeps the buffer under the limit, add it
            buffer = f"{buffer} {sentence}".strip()
        else:
            # Case 2: Store the buffer and start a new one with the current sentence
            if buffer:
                result.append(buffer)
            buffer = sentence

    if buffer:
        result.append(buffer)  # Add the last buffer if any

    return result


@dataclass
class InsertTextWithEmbeddingsIntoMilvusInput:
    """Dataclass for the input of inserting text with embeddings."""

    text: str
    embedding: Sequence[float]
    timestamp_unix: int


class InsertTextWithEmbeddingsIntoMilvusInputRes(TypedDict):
    """TypedDict for the response of inserting text with embeddings."""

    insert_count: int
    ids: List[int]


def insert_text_with_embeddings_into_milvus(  # noqa: WPS234
    milvus_client: MilvusClient,
    text_with_embeddings: Sequence[InsertTextWithEmbeddingsIntoMilvusInput],
) -> InsertTextWithEmbeddingsIntoMilvusInputRes:
    """
    Inserts the text with embeddings into the milvus db.

    :param milvus_client: client to make queries to milvus
    :param text_with_embeddings: list of texts with their embeddings
    :returns: Dict of result
    """
    data = []
    for txt_emb in text_with_embeddings:
        data.append(asdict(txt_emb))

    return milvus_client.insert(collection_name="text_embeddings_schema", data=data)


class GetTextsMatchingVectorResEntity(TypedDict):
    """Get texts matching vector res entity."""

    text: str


class GetTextsMatchingVectorRes(TypedDict):
    """TypedDict for the response of inserting text with embeddings."""

    id: int
    distance: float
    entity: GetTextsMatchingVectorResEntity


def get_texts_matching_vector_search(
    milvus_client: MilvusClient,
    embedding_to_match: Sequence[float],
) -> List[GetTextsMatchingVectorRes]:
    """
    Retrieves top 10 results matching the embeddings.

    :param milvus_client: client to make queries to milvus
    :param embedding_to_match: embeddings to match search against with
    :returns: List of TypedDict
    """
    results = milvus_client.search(
        collection_name="text_embeddings_schema",
        data=[embedding_to_match],
        anns_field="embedding",
        output_fields=["text"],
        limit=10,
        timeout=3000,  # noqa: WPS432
    )

    return results[0]
