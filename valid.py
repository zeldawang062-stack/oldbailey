import pandas as pd
from pathlib import Path
from parse_xml import parse_xml
import pandas as pd
folder = Path("sessionsPapers")
xml_files = list(folder.glob("*.xml"))

df_charge = pd.read_parquet("output/charges.parquet")
df_defendant = pd.read_parquet("output/defendants.parquet")

charge_ids = set(df_charge["defendant_id"])
defendant_ids = set(df_defendant["id"])

orphan_ids = charge_ids - defendant_ids

occ = {}
print(len(orphan_ids))

for orphan in orphan_ids:
    occ[orphan] = 0

for file in xml_files:
    text= file.read_text(encoding="utf-8")
    for orphan in orphan_ids:
        occur = text.count(orphan)
        occ[orphan] += occur
print(occ)


import xml.etree.ElementTree as ET
source_person_ids = set()

for file in xml_files:
    tree = ET.parse(file)
    root = tree.getroot()
    for person in root.iter("persName"):
        person_id = person.get("id")

        if person_id is not None:
            source_person_ids.add(person_id)


missing = orphan_ids - source_person_ids

found = orphan_ids & source_person_ids
print("Missing:", len(missing))
print("Found:", len(found))
print(missing)
print(found)

print("\nChecking the 14 found IDs:")

for file in xml_files:
    tree = ET.parse(file)
    root = tree.getroot()

    for person in root.iter("persName"):
        person_id = person.get("id")

        if person_id in found:
            print(
                "ID:", person_id,
                "| type:", person.get("type")
            )