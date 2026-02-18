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
- [DASL Client Documentation](https://antimatter-dasl-client.readthedocs-hosted.com/en/latest/) - Python client library for interacting with DASL services

## Repository Structure

```
preset_tool/
├── notebooks/              # Databricks notebooks for interactive preset testing
│   ├── <source>-<source_type>-TEMPLATE-autoloader.py  # Template for file-based ingestion
│   ├── <source>-<source_type>-TEMPLATE-table.py       # Template for table-based ingestion
│   └── <source>-<source_type>.py
├── yaml/                   # Preset YAML configuration files
│   ├── <source>-<source_type>-TEMPLATE.yaml
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

1. Choose the appropriate template:
   - **`<source>-<source_type>-TEMPLATE-autoloader.py`** - For reading from file-based sources (autoloader)
   - **`<source>-<source_type>-TEMPLATE-table.py`** - For reading from existing Delta tables

2. **Import the template into Databricks**:
   - **⚠️ IMPORTANT: Do NOT clone the template notebook in Databricks!** Cloning can cause `UNSUPPORTED_OPERATION` errors due to retained metadata/state.
   - **Recommended approach**: 
     1. Create a **new notebook** in Databricks
     2. Open the template file (e.g., `notebooks/<source>-<source_type>-TEMPLATE-autoloader.py`) in your editor
     3. Copy all the code from the template
     4. Paste it into your new Databricks notebook
   - Alternatively, you can copy the template file locally:
     ```bash
     cp notebooks/<source>-<source_type>-TEMPLATE-autoloader.py notebooks/<source>-<source_type>.py
     # OR
     cp notebooks/<source>-<source_type>-TEMPLATE-table.py notebooks/<source>-<source_type>.py
     cp yaml/<source>-<source_type>-TEMPLATE.yaml yaml/<source>-<source_type>.yaml
     ```

3. Add sample log files to `raw_logs/` directory (if using autoloader mode)

4. Update the notebook:
   - Set your user path in the `%pip install` command
   - Update all values marked with `# CHANGE ME!!!`

5. Configure the YAML preset file (see [Preset Structure Guide](https://docs.sl.antimatter.io/ingest-data/presets/preset-development/preset-structure))

### 2. Test Your Preset

1. Open your copied notebook in Databricks
2. Update all values marked with `# CHANGE ME!!!`:
   - **yaml_string**: Your preset YAML (inline or load from file)
   - **For autoloader template**: `set_autoloader_location`, `set_checkpoint_temp_location_base`, `set_autoloader_temp_schema_location`
   - **For table template**: `set_table` (temp locations are already set to empty strings)
   - **set_input_record_limit**: Maximum number of records to process
   - **evaluate**: Target Unity Catalog location (e.g., `catalog.database`)
3. Run all cells to preview transformations and validate outputs
4. Iterate on the YAML configuration as needed

### 3. Deploy to Production

Once your preset is validated and working correctly:

1. Commit your YAML preset file
2. Deploy using [DSL Lite](https://github.com/grp-db/dsl_lite) following its deployment instructions

## Usage Examples

### Autoloader Mode (File-based Ingestion)

Use the `-autoloader` template for reading from file-based sources:

**Note**: The paths shown below are **sample placeholder paths** for illustration only. You must replace them with your actual paths. Your paths may be different (e.g., different Volume names, directory structures, etc.). Replace all placeholders like `<path>`, `<source>`, `<source_type>`, and `<user>` with your actual values.

```python
# Load YAML - Option 1: Define inline
yaml_string = """
name: my_preset
description: "My preset description"
# ... rest of your YAML ...
"""

# Load YAML - Option 2: Load from file (uncomment to use)
# with open("/Workspace/Users/<user>/preset_tool/yaml/<source>-<source_type>.yaml", 'r') as file:
#     yaml_string = file.read()

from dasl_client.preset_development import PreviewParameters, PreviewEngine

ds_params = (PreviewParameters(spark) 
    .from_autoloader()  
    .set_autoloader_location("/Volumes/<path>/logs/<source>/<source_type>/") # CHANGE ME!!!
    .set_checkpoint_temp_location_base("/Volumes/<path>/tmp/checkpoints/<source>-<source_type>.cp") # CHANGE ME!!!
    .set_autoloader_temp_schema_location("/Volumes/<path>/tmp/schemas/<source>-<source_type>.json") # CHANGE ME!!!
    .set_input_record_limit(10000) # CHANGE ME!!!
)

ps = PreviewEngine(spark, yaml_string, ds_params)
ps.evaluate("catalog.database") # CHANGE ME!!!
```

### Table Mode (Delta Table Ingestion)

Use the `-table` template for reading from existing Delta tables:

**Note**: The paths and table names shown below are **sample placeholder values** for illustration only. You must replace them with your actual values. Your catalog, database, and table names will be different. Replace all placeholders like `<user>` and `catalog.database.table` with your actual Unity Catalog paths.

```python
# Load YAML - Option 1: Define inline
yaml_string = """
name: my_preset
description: "My preset description"
# ... rest of your YAML ...
"""

# Load YAML - Option 2: Load from file (uncomment to use)
# with open("/Workspace/Users/<user>/preset_tool/yaml/<source>-<source_type>.yaml", 'r') as file:
#     yaml_string = file.read()

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
```

**Note**: When using `from_table()`, you must set `set_checkpoint_temp_location_base` and `set_autoloader_temp_schema_location` to empty strings (`""`) to avoid Configuration errors.

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

**Issue**: When using `from_table()` mode, you must set `set_checkpoint_temp_location_base` and `set_autoloader_temp_schema_location` to empty strings (`""`) to avoid a Configuration error.

**Workaround**: The `-table` template notebook already sets these values to empty strings. If you're using the table template, this is already handled for you.

**Note**: This is a limitation of the preview tool. When deploying via DSL Lite, this workaround is not needed.

### 3. `UNSUPPORTED_OPERATION: data type is not supported` Error

**Issue**: You may encounter `[UNSUPPORTED_OPERATION] data type is not supported` error.

**Known Causes**:
- **⚠️ CLONING NOTEBOOK TEMPLATES**: **This is the primary cause!** Cloning the template notebook can cause this error due to retained metadata, execution state, or cached schema information from the original template. The same code works perfectly when creating a fresh notebook and manually pasting the code.
- **Databricks widgets and variables passed as parameters**: Using Databricks widgets or Python variables passed as parameters to `PreviewParameters` methods can cause this error, even when the values are correct. This appears to be a limitation with how the preview engine handles parameterized inputs.
- Empty or invalid autoloader path (path doesn't exist or contains no data files)
- Invalid or empty YAML
- Empty schema (data source has no files)

**Workaround**: 
- **⚠️ DO NOT CLONE THE TEMPLATE NOTEBOOK** - Instead, create a new notebook and manually copy/paste the code from the template file. This is the most reliable workaround.
- **Do NOT use widgets or variables for parameters** - Instead, hardcode the values directly in the method calls (e.g., `.set_autoloader_location("/Volumes/path/to/logs/")` instead of `.set_autoloader_location(widget_value)`)
- Use the template notebooks which use hardcoded values that you can directly edit
- If you must use variables, try creating a completely fresh notebook and manually typing the code (avoid copying from template)

**Troubleshooting**:
- **First step**: Create a new notebook (don't clone) and manually paste the template code
- Verify the autoloader path exists and has data: `dbutils.fs.ls("/your/path")`
- Ensure YAML is valid and not empty
- If cloning is necessary, try clearing all cell outputs and restarting the Python kernel before running

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
