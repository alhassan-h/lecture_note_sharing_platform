"""
Supabase client initialization and helper functions.
Provides storage bucket access for uploading and downloading lecture notes.
"""

import os
from supabase import create_client, Client

# Initialize Supabase client if credentials are available
def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.
    Requires SUPABASE_URL and SUPABASE_KEY environment variables.
    """
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables are required for Supabase integration."
        )
    
    return create_client(supabase_url, supabase_key)

def upload_to_supabase(file_content: bytes, file_path: str, bucket_name: str = 'lecture-notes') -> str:
    """
    Upload a file to Supabase Storage.
    
    Args:
        file_content: The file content as bytes
        file_path: The path to store the file in the bucket (e.g., 'uploads/file123.pdf')
        bucket_name: The bucket name (default: 'lecture-notes')
    
    Returns:
        The full URL of the uploaded file
    """
    try:
        supabase = get_supabase_client()
        response = supabase.storage.from_(bucket_name).upload(file_path, file_content)
        
        # Return the public URL for the uploaded file
        return supabase.storage.from_(bucket_name).get_public_url(file_path)
    except Exception as e:
        raise Exception(f"Failed to upload file to Supabase: {str(e)}")

def download_from_supabase(file_path: str, bucket_name: str = 'lecture-notes') -> bytes:
    """
    Download a file from Supabase Storage.
    
    Args:
        file_path: The path of the file in the bucket
        bucket_name: The bucket name (default: 'lecture-notes')
    
    Returns:
        The file content as bytes
    """
    try:
        supabase = get_supabase_client()
        response = supabase.storage.from_(bucket_name).download(file_path)
        return response
    except Exception as e:
        raise Exception(f"Failed to download file from Supabase: {str(e)}")

def delete_from_supabase(file_path: str, bucket_name: str = 'lecture-notes') -> None:
    """
    Delete a file from Supabase Storage.
    
    Args:
        file_path: The path of the file in the bucket
        bucket_name: The bucket name (default: 'lecture-notes')
    """
    try:
        supabase = get_supabase_client()
        supabase.storage.from_(bucket_name).remove([file_path])
    except Exception as e:
        raise Exception(f"Failed to delete file from Supabase: {str(e)}")

def get_supabase_signed_url(file_path: str, bucket_name: str = 'lecture-notes', expires_in: int = 3600) -> str:
    """
    Generate a signed URL for a file in Supabase Storage.
    Useful for temporary access to private files.
    
    Args:
        file_path: The path of the file in the bucket
        bucket_name: The bucket name (default: 'lecture-notes')
        expires_in: URL expiration time in seconds (default: 3600 = 1 hour)
    
    Returns:
        The signed URL for the file
    """
    try:
        supabase = get_supabase_client()
        response = supabase.storage.from_(bucket_name).create_signed_url(file_path, expires_in)
        return response['signedURL']
    except Exception as e:
        raise Exception(f"Failed to generate signed URL: {str(e)}")
