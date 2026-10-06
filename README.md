# Old Bailey Historical Court Records Data Pipeline

An end-to-end data engineering pipeline that transforms historical Old Bailey court records from XML into analytics-ready Parquet datasets, uploads curated data to Amazon S3, catalogs the schema with AWS Glue, and enables querying with Amazon Athena.

## Tech Stack

- Python
- Pandas
- Parquet
- Amazon S3
- AWS Glue
- Amazon Athena
- boto3

## Pipeline Overview

Old Bailey XML
→ Python XML Parser
→ Relational Tables
→ Processed Parquet
→ Data Quality & Deduplication
→ Curated Parquet
→ Amazon S3
→ AWS Glue Data Catalog
→ Amazon Athena

## Project Structure

```text
oldbailey/
├── parse_xml.py
├── extract.py
├── transform.py
├── upload.py
├── crawler.py
├── pipeline.py
├── valid.py
├── requirements.txt
├── .gitignore
├── README.md
├── sessionsPapers/   # raw XML data, not tracked by Git
├── output/           # processed Parquet, generated locally
└── curated/          # cleaned/curated Parquet, generated locally


然后再加一个 **Data Quality & Transformation**：

```md
##Data Quality & Transformation

The pipeline preserves source inconsistencies instead of silently discarding conflicting records.

Transformation steps include:
- Removing exact duplicate rows
- Detecting duplicate record IDs after exact deduplication
- Adding a `has_conflict` boolean flag to ID-bearing tables
- Preserving conflicting source records for downstream inspection
- Validating referential integrity across relational tables

Tables with record-level conflict detection:
- `defendants`
- `offences`
- `verdicts`
- `punishments`
- `charges`
`defendant_punishments` does not contain its own unique record ID, so no `has_conflict` column is added.

## Architecture
The pipeline separates local data processing from cloud-based storage and querying.

### 1. Extract
`extract.py` reads the raw Old Bailey XML files from `sessionsPapers/` and uses `parse_xml.py` to convert semi-structured XML into six relational datasets.

The extracted tables are written as Parquet files to `output/`.

### 2. Transform
`transform.py` reads the processed Parquet files, removes exact duplicate rows, detects conflicting duplicate IDs, and adds a `has_conflict` flag where applicable.

The curated datasets are written to `curated/`.

### 3. Load
`upload.py` uploads the curated Parquet datasets to Amazon S3 using `boto3`.
Each table is stored under its own S3 prefix: s3://old-baily-cases-study/curated/<table_name>/

###4. Catalog
crawler.py triggers the AWS Glue crawler oldBailey.
The crawler scans the curated S3 data and updates the AWS Glue Data Catalog with table schemas and metadata.

###5. Query
Amazon Athena uses the Glue Data Catalog metadata to query the Parquet files directly from S3 using SQL.

###6. Orchestration
pipeline.py runs the local ETL steps in sequence:
Extract
→ Transform
→ Upload to S3
→ Trigger Glue Crawler
The pipeline currently confirms that the crawler was successfully triggered, but does not wait for the crawler execution to finish.




## Data Model

The XML source is normalized into six relational tables:

- `defendants`
- `offences`
- `verdicts`
- `punishments`
- `charges`
- `defendant_punishments`
`charges` links defendants, offences, and verdicts:

charges
├── charge_id
├── targOrder
├── defendant_id  → defendants.id
├── offence_id    → offences.id
└── verdict_id    → verdicts.id

defendant_punishments links defendants to punishments:
defendant_punishments
├── result
├── targOrder
├── defendant_id   → defendants.id
└── punishment_id  → punishments.id

Because the historical XML contains irregular references and inconsistent identifiers, referential integrity is validated but source inconsistencies are preserved rather than force-corrected.

## Data Quality Findings

Validation identified several source-level inconsistencies and reference irregularities in the historical XML dataset.

### Referential Integrity

Distinct orphan references found during validation:

| Relationship                                            |Orphan IDs |
|---------------------------------------------------------|-----------|
| `charges.defendant_id → defendants.id`                  | 87        |
| `charges.offence_id → offences.id`                      | 352       |
| `charges.verdict_id → verdicts.id`                      | 657       |
| `defendant_punishments.defendant_id → defendants.id`    | 13        |
| `defendant_punishments.punishment_id → punishments.id`  | 0         |

Further inspection of the 87 orphan `defendant_id` values found that:

- 73 do not exist in any source `<persName>` identifier
- 14 exist in the XML but are associated with other person types such as `victimName`, `judiciaryName`, or unspecified types

This suggests a combination of source/reference irregularities and limitations in the current parser assumption that the first target of a `criminalCharge` always represents a defendant.

### Duplicate and Conflict Detection

Exact duplicate rows are removed first. Records sharing the same ID but containing different values are preserved and flagged using `has_conflict = True`.

Post-deduplication conflicting IDs:

| Table | Conflicting IDs |
|-------|-----------------|
| `defendants` | 0  |
| `offences`   | 59 |
| `verdicts`   | 208|
| `punishments`| 0  |
| `charges`    | 194|

This approach avoids arbitrarily selecting one version of an inconsistent historical record.
