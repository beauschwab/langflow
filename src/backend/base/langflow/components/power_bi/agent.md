# components/power_bi/ — Power BI & Microsoft Fabric Components

## Purpose
Microsoft Power BI and Fabric integration for executing DAX queries, managing datasets, and orchestrating Fabric notebook runs.

## Key Files

| File | Description |
|------|-------------|
| `power_bi_dax_query.py` | Execute a DAX query against a Power BI semantic model and return results as `list[Data]`. Primary use case for dataframe-based analysis flows. |
| `power_bi_list_datasets.py` | List all datasets (semantic models) in a Power BI workspace and return IDs and metadata. |
| `power_bi_refresh_dataset.py` | Trigger an on-demand refresh of a Power BI dataset and return HTTP status. |
| `fabric_run_notebook.py` | Run a Microsoft Fabric notebook, optionally waiting for completion and returning job status. |

## Authentication

All components use **Azure AD client-credentials** flow:

| Input | Description |
|-------|-------------|
| Tenant ID | Azure AD directory ID |
| Client ID | Azure AD app registration client ID |
| Client Secret | Azure AD app registration secret |

The Power BI components acquire tokens against `https://analysis.windows.net/powerbi/api/.default`.  
The Fabric notebook component acquires tokens against `https://api.fabric.microsoft.com/.default`.

### Required Azure AD App Permissions

| Component | Required permission |
|-----------|---------------------|
| DAX Query, List Datasets, Refresh | `Dataset.ReadWrite.All` (Power BI Service) |
| Run Notebook | `Item.Execute.All` (Microsoft Fabric) |

> **Note:** Service-principal access must be enabled in the Power BI tenant admin settings under *Allow service principals to use Power BI APIs*.

## DAX Query — Primary Use Case

The `PowerBIDAXQueryComponent` is the core component for analytical flows:

1. Connect to any Power BI semantic model by workspace ID + dataset ID.
2. Provide a DAX expression in the *DAX Query* field.
3. Results are returned as `list[Data]` — each item is one result row with column names cleaned of table-qualifier prefixes.
4. Pipe results into a Python component to convert to a pandas DataFrame for further processing, visualisation, or downstream flow steps.

**Example DAX query:**
```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Date'[Year],
    'Date'[Month],
    "Total Sales", SUM(Sales[Amount]),
    "Transaction Count", COUNTROWS(Sales)
)
```

## Dataset IDs

Use `PowerBIListDatasetsComponent` to enumerate datasets in a workspace.  The returned `dataset_id` field can be wired directly into `PowerBIDAXQueryComponent` or `PowerBIRefreshDatasetComponent`.

## Component Discovery

Components are auto-discovered by Langflow's folder-scanning mechanism — no manual registration is required.
