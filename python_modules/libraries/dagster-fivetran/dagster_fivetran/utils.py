from typing import Any, Dict, Iterator, Mapping, Optional, Sequence

import dagster._check as check
from dagster import AssetMaterialization, MetadataValue
from dagster._core.definitions.metadata import RawMetadataMapping
from dagster._core.definitions.metadata.metadata_set import TableMetadataSet
from dagster._core.definitions.metadata.table import TableColumn, TableSchema

from dagster_fivetran.types import FivetranOutput


def get_fivetran_connector_url(connector_details: Mapping[str, Any]) -> str:
    service = connector_details["service"]
    schema = connector_details["schema"]
    return f"https://fivetran.com/dashboard/connectors/{service}/{schema}"


def get_fivetran_logs_url(connector_details: Mapping[str, Any]) -> str:
    return f"{get_fivetran_connector_url(connector_details)}/logs"


def get_fivetran_connector_table_name(schema_name: str, table_name: str) -> str:
    return f"{schema_name}.{table_name}"


# TODO: move to translator.py and make table_data a FivetranTable object
def metadata_for_table(
    table_data: Mapping[str, Any],
    connector_url: str,
    database: Optional[str],
    schema: Optional[str],
    table: Optional[str],
    include_column_info: bool = False,
) -> RawMetadataMapping:
    metadata: Dict[str, MetadataValue] = {"connector_url": MetadataValue.url(connector_url)}
    column_schema = None
    table_name = None
    if table_data.get("columns"):
        columns = check.dict_elem(table_data, "columns")
        table_columns = sorted(
            [
                TableColumn(name=col["name_in_destination"], type="")
                for col in columns.values()
                if "name_in_destination" in col and col.get("enabled")
            ],
            key=lambda col: col.name,
        )
        column_schema = TableSchema(columns=table_columns)

        if include_column_info:
            metadata["column_info"] = MetadataValue.json(columns)

    if database and schema and table:
        table_name = ".".join([database, schema, table])
    metadata = {
        **TableMetadataSet(column_schema=column_schema, table_name=table_name),
        **metadata,
    }

    return metadata


def _table_data_to_materialization(
    fivetran_output: FivetranOutput,
    asset_key_prefix: Sequence[str],
    schema_name: str,
    schema_source_name: str,
    table_source_name: str,
    table_data: Mapping[str, Any],
) -> Optional[AssetMaterialization]:
    table_name = table_data["name_in_destination"]
    asset_key = [*asset_key_prefix, schema_name, table_name]
    if not table_data["enabled"]:
        return None

    return AssetMaterialization(
        asset_key=asset_key,
        description=f"Table generated via Fivetran sync: {schema_name}.{table_name}",
        metadata={
            **metadata_for_table(
                table_data,
                get_fivetran_connector_url(fivetran_output.connector_details),
                include_column_info=True,
                database=None,
                schema=schema_name,
                table=table_name,
            ),
            "schema_source_name": schema_source_name,
            "table_source_name": table_source_name,
        },
    )


def generate_materializations(
    fivetran_output: FivetranOutput,
    asset_key_prefix: Sequence[str],
) -> Iterator[AssetMaterialization]:
    for schema_source_name, schema in fivetran_output.schema_config["schemas"].items():
        schema_name = schema["name_in_destination"]
        schema_prefix = fivetran_output.connector_details.get("config", {}).get("schema_prefix")
        if schema_prefix:
            schema_name = f"{schema_prefix}_{schema_name}"
        if not schema["enabled"]:
            continue

        for table_source_name, table_data in schema["tables"].items():
            if not table_data["enabled"]:
                continue

            mat = _table_data_to_materialization(
                fivetran_output=fivetran_output,
                asset_key_prefix=asset_key_prefix,
                schema_name=schema_name,
                table_data=table_data,
                schema_source_name=schema_source_name,
                table_source_name=table_source_name,
            )
            if mat is not None:
                yield mat
