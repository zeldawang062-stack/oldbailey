import pandas as pd
from pathlib import Path

def transform():
    folder = Path("output")
    output_path = Path("curated")
    output_path.mkdir(exist_ok=True)
    parquet_files = list(folder.glob("*.parquet"))
    for file in parquet_files:
        df = pd.read_parquet(file)
        df_clean=df.drop_duplicates()
        df_clean.to_parquet(
        output_path / file.name,
        index=False)

        before = len(df)
        after = len(df_clean)

        print(file.name, "removed:", before - after)

    folder2 = Path("curated")
    parquet_files_curated = list(folder2.glob("*.parquet"))

    id_columns = {
        "defendants.parquet": "id",
        "offences.parquet": "id",
        "verdicts.parquet": "id",
        "punishments.parquet": "id",
        "charges.parquet": "charge_id"
    }
    print([file.name for file in parquet_files_curated])
    for file in parquet_files_curated:

        # defendant_punishments 没有自己的 ID，暂时跳过
        if file.name not in id_columns:
            continue

        df = pd.read_parquet(file)

        id_column = id_columns[file.name]

        duplicates = df[id_column].value_counts()
        duplicates = duplicates[duplicates > 1]
        df["has_conflict"] = df[id_column].isin(duplicates.index)
        df.to_parquet(file,index=False)

        print("\n", file.name)
        print("Conflicting IDs:", len(duplicates))
    

