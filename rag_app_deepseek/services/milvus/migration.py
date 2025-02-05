from pymilvus import Collection, CollectionSchema, connections, db, utility

from rag_app_deepseek.services.milvus.schema import text_embeddings_schema
from rag_app_deepseek.settings import settings


def has_db(name: str) -> bool:
    """
    Checks if db already exists.

    :param name: name of the database
    :returns: if db already exists or not.
    """
    return name in db.list_database()


def create_db(name: str) -> None:
    """
    Creates the db with provided name.

    :param name: name of the database
    :returns: None
    """
    return db.create_database(db_name=name)


def has_collection(name: str) -> bool:
    """
    Checks if the collection exists.

    :param name: name of the collection
    :returns: if the collection already exists or not.
    """
    return utility.has_collection(collection_name=name)


def create_collection(name: str, schema: CollectionSchema) -> Collection:
    """
    Creates a new collection with provided name and schema.

    :param name: name of the collection
    :param schema: schema of the collection to create
    :returns: the newly created collection.
    """
    collection = Collection(name=name, data=None, schema=schema)
    print("\ncollection created:", name)  # noqa: WPS421
    return collection


def ensure_db_and_collections():  # type: ignore
    """Ensures if the db and collections exists."""
    connections.connect(
        host=settings.milvus_host,
        port=settings.milvus_port,
        user=settings.milvus_username,
        password=settings.milvus_password,
        keep_alive=True,
        db_name=settings.milvus_db_name,
    )
    print("milvus connected", settings.milvus_host)  # noqa: WPS421

    does_db_exists = has_db(settings.milvus_db_name)

    if not does_db_exists:
        create_db(settings.milvus_db_name)

    does_text_embeddings_coll_exists = has_collection("text_embeddings_schema")
    if does_text_embeddings_coll_exists is False:
        create_collection(name="text_embeddings_schema", schema=text_embeddings_schema)

    connections.disconnect(settings.milvus_conn_name)
    print("milvus disconnected")  # noqa: WPS421


ensure_db_and_collections()
