# Databricks notebook source
# MAGIC # ⚠️ IMPORTANT: Do NOT clone this notebook in Databricks!
# MAGIC # Create a NEW notebook and paste this code instead to avoid UNSUPPORTED_OPERATION errors.
# MAGIC # See README.md for details.
# MAGIC %pip install /Workspace/Users/<first.last@email.com>/preset_tool/lib/*.whl
# MAGIC # Alternative: Install from PyPI if wheel files are not available locally
# MAGIC # MAGIC %pip install dasl-client dasl-api
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# Load YAML - Option 1: Define inline
yaml_string = """
# CHANGE ME!!! Paste your YAML here
"""

# Load YAML - Option 2: Load from file (uncomment to use)
# with open("/Workspace/Users/<user>/preset_tool/yaml/<source>-<source_type>.yaml", 'r') as file:
#     yaml_string = file.read()

# COMMAND ----------

from dasl_client.preset_development import PreviewParameters, PreviewEngine

ds_params = (PreviewParameters(spark)
    .from_table()
    .set_table("catalog.database.table") # CHANGE ME!!!
    .set_checkpoint_temp_location_base("")  # Must be empty string
    .set_autoloader_temp_schema_location("")  # Must be empty string
    .set_input_record_limit(10000) # CHANGE ME!!!
)

ps = PreviewEngine(spark, yaml_string, ds_params)
ps.evaluate("catalog.database") # CHANGE ME!!!

