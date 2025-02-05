from pymilvus import CollectionSchema, DataType, FieldSchema

text_embeddings_field_primary_key = FieldSchema(
    name="id",
    dtype=DataType.INT64,
    is_primary=True,
    auto_id=True,
)

text_embeddings_field_embedding = FieldSchema(
    name="vector",
    dtype=DataType.FLOAT_VECTOR,
    dim=768,  # noqa: WPS432
)

text_embeddings_field_text = FieldSchema(
    name="text",
    dtype=DataType.VARCHAR,
    max_length=200,  # noqa: WPS432
    description="raw text",
)

text_embeddings_field_timestamp_unix = FieldSchema(
    name="timestamp_unix",
    dtype=DataType.INT64,
    description="stores timestamp of text in unix",
)

text_embeddings_schema = CollectionSchema(
    fields=[
        text_embeddings_field_primary_key,
        text_embeddings_field_embedding,
        text_embeddings_field_text,
        text_embeddings_field_timestamp_unix,
    ],
    description="text_embeddings_schema",
)
