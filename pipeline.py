from extract import extract
from transform import transform
from upload import upload
from crawler import crawler

print("Starting pipeline...")

print("\n[1/4] Extracting XML...")
extract()

print("\n[2/4] Transforming data...")
transform()

print("\n[3/4] Uploading curated data to S3...")
upload()


print("\n[4/4] Starting Glue crawler...")
crawler()

print("\nPipeline complete!")