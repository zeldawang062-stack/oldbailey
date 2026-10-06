import boto3
from pathlib import Path

def upload():
    s3 = boto3.client("s3")

    output_folder = Path("curated")
    parquet_files = list(output_folder.glob("*.parquet"))

    for file in parquet_files:
        bucket_name = "old-baily-cases-study"

        s3.upload_file(
            file,
            bucket_name,
            "curated/" + file.stem + "/" + file.name
        )

    print("upload completed")