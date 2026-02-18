# DASL Preset Tool

Databricks Antimatter Security Lakehouse is a preset development tool for interactive testing and preparation of cyber data pipelines before deployment to production. The [DSL Lite](https://github.com/grp-db/dsl_lite) accelerator can be used to deploy YAMLs built via DASL as Spark data pipelines.

## Overview

This repository provides a local development workflow for creating, testing, and iterating on preset configurations. Use the interactive notebook-based tool to preview transformations, validate OCSF schema outputs, and debug preset logic before deploying to your production pipeline.

## Purpose

1. **Interactive Development**: Test preset transformations in real-time using sample log files
2. **Rapid Iteration**: Quickly validate changes to YAML preset configurations
3. **Preview & Debug**: Preview bronze, silver, and gold layer outputs before deployment
4. **Production Deployment**: Once validated, deploy presets via [DSL Lite](https://github.com/grp-db/dsl_lite)

## Documentation

For comprehensive preset development documentation, see:
- [Preset Development Landing Page](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-dev-landing-page)
- [Preset Structure Guide](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-structure)
- [Preset Template](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-template)

## Repository Structure

```
preset_tool/
├── notebooks/              # Databricks notebooks for interactive preset testing
│   ├── <source>-<source_type>.py-TEMPLATE
│   └── <source>-<source_type>.py
├── yaml/                   # Preset YAML configuration files
│   ├── <source>-<source_type>.yaml-TEMPLATE
│   └── <source>-<source_type>.yaml
├── raw_logs/               # Sample log files for testing
│   └── <source>-<source_type>-sample.*
└── lib/                    # Required Python wheels
    ├── dasl_api-*.whl
    └── dasl_client-*.whl
```

## Dependencies

This tool requires two Python libraries that are included as wheel files in the `lib/` directory:

- **[dasl-api](https://pypi.org/project/dasl-api/)** - DASL API library for preset development
- **[dasl-client](https://pypi.org/project/dasl-client/)** - DASL client library for interacting with DASL services

### Current Versions

The repository includes pre-packaged wheel files:
- `dasl_api-0.1.30-py3-none-any.whl`
- `dasl_client-1.0.34-py3-none-any.whl`

### Installing/Updating Dependencies

The notebooks automatically install these libraries from the local `lib/` directory. To update to newer versions:

1. Download the latest wheel files from PyPI:
   - [dasl-api on PyPI](https://pypi.org/project/dasl-api/#files)
   - [dasl-client on PyPI](https://pypi.org/project/dasl-client/#files)

2. Replace the wheel files in the `lib/` directory

3. Alternatively, install directly from PyPI in your notebook:
   ```python
   %pip install dasl-api dasl-client
   ```

## Getting Started

### 1. Create a New Preset

1. Copy the template files:
   ```bash
   cp notebooks/<source>-<source_type>.py-TEMPLATE notebooks/<source>-<source_type>.py
   cp yaml/<source>-<source_type>.yaml-TEMPLATE yaml/<source>-<source_type>.yaml
   ```

2. Add sample log files to `raw_logs/` directory

3. Update the notebook:
   - Set your user path in the `%pip install` command
   - Fill in the widget values at the top of the notebook (defaults are empty strings)

4. Configure the YAML preset file (see [Preset Structure Guide](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-structure))

### 2. Test Your Preset

1. Open the notebook in Databricks
2. Configure parameters using the widgets at the top of the notebook (all defaults are empty strings - you must fill them in):
   - **YAML Preset Path**: Path to your preset YAML file (e.g., `/Workspace/Users/<user>/preset_tool/yaml/<source>-<source_type>.yaml`)
   - **Data Source Type**: Dropdown to select "autoloader" (read from files) or "table" (read from Delta table)
   - **Autoloader Location**: Source directory for log files (e.g., `/Volumes/<path>/logs/<source>/<source_type>/`) (required when Data Source Type = "autoloader")
   - **Table Name**: Fully qualified table name `catalog.database.table` (e.g., `<catalog>.<database>.<table>`) (required when Data Source Type = "table")
   - **Autoloader Temp Schema Location**: Temporary location for schema inference (e.g., `/Volumes/<path>/tmp/schemas/`) (autoloader mode only)
   - **Autoloader Temp Checkpoint Location**: Temporary location for streaming checkpoints (e.g., `/Volumes/<path>/tmp/checkpoints/`) (autoloader mode only)
   - **Target Catalog.Database**: Target Unity Catalog location for preview tables (e.g., `<catalog>.<database>`)
   - **Input Record Limit**: Maximum number of records to process (default: 100)
3. Run all cells to:
   - Install required libraries
   - Load the YAML preset configuration
   - Preview transformations on sample data
   - Validate OCSF schema outputs
4. Iterate on the YAML configuration as needed

### 3. Deploy to Production

Once your preset is validated and working correctly:

1. Commit your YAML preset file
2. Deploy using [DSL Lite](https://github.com/grp-db/dsl_lite) following its deployment instructions

## Usage Example

The notebook uses Databricks widgets for interactive configuration. You can set values in the widget panel at the top of the notebook, or the code will use default values:

```python
# Widgets are defined at the top of the notebook (defaults are empty strings - fill them in)
dbutils.widgets.text("yaml_path", "", "YAML Preset Path")
dbutils.widgets.dropdown("data_source", "autoloader", ["autoloader", "table"], "Data Source Type")
dbutils.widgets.text("autoloader_location", "", "Autoloader Location")
dbutils.widgets.text("table_name", "", "Table Name (catalog.database.table)")
dbutils.widgets.text("autoloader_temp_schema_location", "", "Autoloader Temp Schema Location")
dbutils.widgets.text("autoloader_temp_checkpoint_location", "", "Autoloader Temp Checkpoint Location")
dbutils.widgets.text("target_catalog_db", "", "Target Catalog.Database")
dbutils.widgets.text("input_record_limit", "100", "Input Record Limit")

# Get widget values
yaml_path = dbutils.widgets.get("yaml_path")
data_source = dbutils.widgets.get("data_source")
autoloader_location = dbutils.widgets.get("autoloader_location")
table_name = dbutils.widgets.get("table_name")
autoloader_temp_schema_location = dbutils.widgets.get("autoloader_temp_schema_location")
autoloader_temp_checkpoint_location = dbutils.widgets.get("autoloader_temp_checkpoint_location")
target_catalog_db = dbutils.widgets.get("target_catalog_db")
input_record_limit = int(dbutils.widgets.get("input_record_limit"))

from dasl_client.preset_development import PreviewParameters, PreviewEngine

# Load your preset YAML
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
    # Note: When using from_table(), temp locations must be set to empty strings
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
```

**Note**: Widget values can be changed without modifying code, making it easy to test different configurations or switch between presets.

### Example: Using `from_table()` Mode

Here's a direct example of using `from_table()` to preview a preset from an existing Delta table:

```python
from dasl_client.preset_development import PreviewParameters, PreviewEngine

yaml_string = """
name: zeek_conn
description: "Zeek Conn logs"
title: "Zeek Conn"

bronze:
  skipBronzeLoading: true

silver:
  bronzeTables:
    - name: dsl_grp.zeek.zeek_conn_silver
  transform:
    - name: dsl_grp.zeek.zeek_conn_silver
      utils:
        unreferencedColumns:
          preserve: true

gold:
  - name: network_activity
    input: dsl_grp.zeek.zeek_conn_silver
    fields:
      - name: category_uid
        expr: CAST('4' AS INT)
      - name: category_name
        literal: Network Activity
      - name: class_uid
        expr: CAST('4001' AS INT)
      - name: class_name
        literal: Network Activity
      - name: severity_id
        expr: CAST('1' AS INT)
      - name: severity
        literal: Informational
"""

ds_params = (PreviewParameters(spark)
    .from_table()
    .set_table("dsl_grp.zeek.zeek_conn_silver")
    .set_autoloader_temp_schema_location("")
    .set_checkpoint_temp_location_base("")
    .set_input_record_limit(10)
)

ps = PreviewEngine(spark, yaml_string, ds_params)
ps.evaluate("dsl_grp.ocsf")
```

**Note**: When using `from_table()`, you must set `set_autoloader_temp_schema_location` and `set_checkpoint_temp_location_base` to empty strings (`""`) to avoid Configuration errors.

## Known Bugs

### 1. `_metadata.file_path` Not Supported

**Issue**: The `_metadata.file_path` column is not currently supported in the preview tool.

**Workaround**: Comment out or remove any references to `_metadata.file_path` in your preset YAML:

```yaml
bronze:
  name: my_bronze
  preTransform:
    - "*"
    # - "_metadata.file_path"  # Not supported in preview tool
    - other_transformations...
```

**Note**: This limitation only affects the preview tool. `_metadata.file_path` will work correctly when deployed via DSL Lite.

### 2. `from_table()` Requires Empty Temp Locations

**Issue**: When using `from_table()` mode, you must set `set_autoloader_temp_schema_location` and `set_checkpoint_temp_location_base` to empty strings (`""`) to avoid a Configuration error.

**Workaround**: The notebook automatically handles this when you select "table" as the Data Source Type. The code sets these values to empty strings:

```python
if data_source == "table":
    ds_params = (PreviewParameters(spark) 
        .from_table() 
        .set_table(table_name)
        .set_autoloader_temp_schema_location("")  # Must be empty string
        .set_checkpoint_temp_location_base("")     # Must be empty string
        .set_input_record_limit(input_record_limit)
    )
```

**Note**: This is a limitation of the preview tool. When deploying via DSL Lite, this workaround is not needed.

## Related Projects

- **[DSL Lite](https://github.com/grp-db/dsl_lite)**: Production deployment framework for presets
- [Databricks Antimatter Documentation](https://docs.sl.antimatter.io/)

## Support

For issues, questions, or feature requests related to:
- **Preset development**: See [Databricks Antimatter Documentation](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-dev-landing-page)
- **DSL Lite deployment**: See [DSL Lite Repository](https://github.com/grp-db/dsl_lite)

---

## Copyright

**Copyright © Databricks, Inc.**

DASL Preset Dev Tool is developed and maintained by Databricks & Antimatter.
