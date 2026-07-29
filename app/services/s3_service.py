import os
import uuid
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# ============================================
# Load Environment Variables
# ============================================

load_dotenv()

# ============================================
# AWS Configuration
# ============================================

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# ============================================
# Create S3 Client
# ============================================

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# ============================================
# Upload File to Amazon S3
# ============================================

def upload_file_to_s3(file):
    """
    Uploads a file to Amazon S3.

    Parameters:
        file : FileStorage object received from Flask

    Returns:
        file_name : Unique filename stored in S3
    """

    try:
        # Generate unique filename
        file_name = f"{uuid.uuid4()}_{file.filename}"

        # Upload file to S3
        s3_client.upload_fileobj(
            Fileobj=file,
            Bucket=S3_BUCKET_NAME,
            Key=file_name
        )

        return file_name

    except ClientError as e:
        raise Exception(f"S3 Upload Failed: {str(e)}")
    
    