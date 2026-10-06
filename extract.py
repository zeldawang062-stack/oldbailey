from pathlib import Path
from parse_xml import parse_xml
import pandas as pd
def extract():
    folder = Path("sessionsPapers")
    xml_files = list(folder.glob("*.xml"))
    all_defendants = []
    all_offences = []
    all_verdicts = []
    all_punishments = []
    all_charges = []
    all_defpunish = []
    failed_files = []
    for i, path in enumerate(xml_files):
        try:
            result = parse_xml(path)
            all_defendants.append(result[0])
            all_offences.append(result[1])
            all_verdicts.append(result[2])
            all_punishments.append(result[3])
            all_charges.append(result[4])
            all_defpunish.append(result[5])
        except Exception as e:
            print("Failed:", path)
            print("Error!", e)
            failed_files.append(path)
        if i % 500 == 0:
            print("Processed:", i)
    print("Failed files:", len(failed_files))

    df_all_defendants = pd.concat(all_defendants, ignore_index=True)
    df_all_offences = pd.concat(all_offences, ignore_index=True)
    df_all_verdicts = pd.concat(all_verdicts, ignore_index=True)
    df_all_punishments = pd.concat(all_punishments, ignore_index=True)
    df_all_charges = pd.concat(all_charges, ignore_index=True)
    df_all_defpunish = pd.concat(all_defpunish, ignore_index=True)
    print(df_all_defendants.shape)
    print(df_all_offences.shape)
    print(df_all_verdicts.shape)
    print(df_all_punishments.shape)
    print(df_all_charges.shape)
    print(df_all_defpunish.shape)

    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    df_all_defendants.to_parquet(
        output_folder / "defendants.parquet",
        index = False
    )

    df_all_offences.to_parquet(
        output_folder / "offences.parquet",
        index=False
    )

    df_all_verdicts.to_parquet(
        output_folder / "verdicts.parquet",
        index=False
    )

    df_all_punishments.to_parquet(
        output_folder / "punishments.parquet",
        index=False
    )

    df_all_charges.to_parquet(
        output_folder / "charges.parquet",
        index=False
    )

    df_all_defpunish.to_parquet(
        output_folder / "defendant_punishments.parquet",
        index=False
    )

