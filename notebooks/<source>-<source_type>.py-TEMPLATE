# Databricks notebook source
# MAGIC %pip install /Workspace/Users/<first.last@email.com>/preset_tool/lib/*.whl
# MAGIC # Alternative: Install from PyPI if wheel files are not available locally
# MAGIC # MAGIC %pip install dasl-client dasl-api
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configure Preset Preview Parameters
# MAGIC Use the widgets below to configure your preset preview settings.

# COMMAND ----------

dbutils.widgets.text("yaml_path", "", "YAML Preset Path")
dbutils.widgets.dropdown("data_source", "autoloader", ["autoloader", "table"], "Data Source Type")
dbutils.widgets.text("autoloader_location", "", "Autoloader Location")
dbutils.widgets.text("table_name", "", "Table Name (catalog.database.table)")
dbutils.widgets.text("autoloader_temp_schema_location", "", "Autoloader Temp Schema Location")
dbutils.widgets.text("autoloader_temp_checkpoint_location", "", "Autoloader Temp Checkpoint Location")
dbutils.widgets.text("target_catalog_db", "", "Target Catalog.Database")
dbutils.widgets.text("input_record_limit", "100", "Input Record Limit")

# COMMAND ----------

from dasl_client.preset_development import PreviewParameters, PreviewEngine

# Get widget values
yaml_path = dbutils.widgets.get("yaml_path")
data_source = dbutils.widgets.get("data_source")
autoloader_location = dbutils.widgets.get("autoloader_location")
table_name = dbutils.widgets.get("table_name")
autoloader_temp_schema_location = dbutils.widgets.get("autoloader_temp_schema_location")
autoloader_temp_checkpoint_location = dbutils.widgets.get("autoloader_temp_checkpoint_location")
target_catalog_db = dbutils.widgets.get("target_catalog_db")
input_record_limit = int(dbutils.widgets.get("input_record_limit"))

# Load YAML preset file
with open(yaml_path, 'r') as file:
    yaml_string = file.read()

# Configure preview parameters based on data source type
if data_source == "autoloader":
    ds_params = (PreviewParameters(spark) 
        .from_autoloader() 
        .set_autoloader_location(autoloader_location)
        .set_autoloader_temp_schema_location(autoloader_temp_schema_location)
        .set_checkpoint_temp_location_base(autoloader_temp_checkpoint_location)
        .set_input_record_limit(input_record_limit)
    )
elif data_source == "table":
    # Note: When using from_table(), temp locations must be set to empty strings to avoid Configuration error
    ds_params = (PreviewParameters(spark) 
        .from_table() 
        .set_table(table_name)
        .set_autoloader_temp_schema_location("")
        .set_checkpoint_temp_location_base("")
        .set_input_record_limit(input_record_limit)
    )
else:
    raise ValueError(f"Invalid data_source value: '{data_source}'. You must select either 'autoloader' or 'table' from the Data Source Type dropdown.")

# Create preview engine and evaluate
ps = PreviewEngine(spark, yaml_string, ds_params)
ps.evaluate(target_catalog_db)

