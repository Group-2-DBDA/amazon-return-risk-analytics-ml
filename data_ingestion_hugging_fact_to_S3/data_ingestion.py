import sys
import requests
import boto3
from awsglue.utils import getResolvedOptions

# Get Job Arguments

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'target_meta',
    'target_review'
])

meta_target = args['target_meta']
review_target = args['target_review']

s3 = boto3.client('s3')

repo_base = "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/"

meta_files = [
    "raw/meta_categories/meta_Amazon_Fashion.jsonl",
    "raw/meta_categories/meta_Appliances.jsonl",
    "raw/meta_categories/meta_Health_and_Household.jsonl",
    "raw/meta_categories/meta_Musical_Instruments.jsonl"
]

review_files = [
    "raw/review_categories/Amazon_Fashion.jsonl",
    "raw/review_categories/Appliances.jsonl",
    "raw/review_categories/Health_and_Household.jsonl",
    "raw/review_categories/Musical_Instruments.jsonl"
]


# Function: Stream HF → S3

def stream_to_s3(file_path, target_prefix):
    url = repo_base + file_path

    print(f"Streaming {url}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    bucket = target_prefix.replace("s3://", "").split("/")[0]
    key_prefix = "/".join(target_prefix.replace("s3://", "").split("/")[1:])

    key_prefix = key_prefix.rstrip("/")   # <-- FIX HERE

    file_name = file_path.split("/")[-1]
    s3_key = f"{key_prefix}/{file_name}"

    s3.upload_fileobj(response.raw, bucket, s3_key)

    print(f"Uploaded to s3://{bucket}/{s3_key}")


# META Upload

for file in meta_files:
    stream_to_s3(file, meta_target)


# REVIEW Upload

for file in review_files:
    stream_to_s3(file, review_target)

print("All files successfully streamed to S3 🚀")