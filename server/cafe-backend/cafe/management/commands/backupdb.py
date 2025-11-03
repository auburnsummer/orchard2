import asyncio
import sqlite3
from datetime import datetime
from io import BytesIO
from pathlib import Path

from aiohttp import ClientSession
from aiohttp_s3_client import S3Client
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Backs up the SQLite database to S3 using the SQLite Online Backup API
    """
    help = "Backs up the SQLite database to S3"

    def add_arguments(self, parser):
        parser.add_argument(
            '--label',
            type=str,
            default=None,
            help='Custom label for the backup (default: current date YYYY-MM-DD)'
        )

    @async_to_sync
    async def backup_to_s3(self, backup_file_path: str, label: str):
        """Upload the backup to S3"""
        from http import HTTPStatus
        
        BUF_SIZE = 65536  # 64kb chunks
        
        async def file_generator():
            """Generator to read file in chunks"""
            with open(backup_file_path, 'rb') as f:
                while True:
                    chunk = f.read(BUF_SIZE)
                    if not chunk:
                        break
                    yield chunk
        
        # Get the file size
        file_size = Path(backup_file_path).stat().st_size
        
        async with ClientSession(raise_for_status=True) as session:
            client = S3Client(
                url=settings.S3_BACKUP_API_URL,
                session=session,
                access_key_id=settings.S3_BACKUP_ACCESS_KEY_ID,
                secret_access_key=settings.S3_BACKUP_SECRET_ACCESS_KEY,
                region=settings.S3_BACKUP_REGION
            )
            
            # Upload the backup with a descriptive filename
            filename = f"db-backup-{label}.sqlite3"
            
            async with client.put(
                filename,
                file_generator(),
                data_length=file_size
            ) as resp:
                if resp.status != HTTPStatus.OK:
                    raise Exception(f"Failed to upload backup to S3: {resp.status}")
            
            return filename

    def handle(self, *args, **options):
        # Get the label for the backup
        label = options['label']
        if label is None:
            label = datetime.now().strftime('%Y-%m-%d')
        
        self.stdout.write(f"Starting database backup with label: {label}")
        
        # Get the database path from settings
        db_path = settings.DATABASES['default']['NAME']
        
        if not Path(db_path).exists():
            self.stdout.write(
                self.style.ERROR(f"Database file not found at {db_path}")
            )
            return
        
        try:
            # Create a temporary file to backup to
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite3') as temp_file:
                temp_path = temp_file.name
            
            # Use SQLite's Online Backup API to backup directly to the temporary file
            # This ensures a consistent snapshot even if the database is being written to
            source_conn = sqlite3.connect(db_path)
            backup_conn = sqlite3.connect(temp_path)
            
            with source_conn:
                source_conn.backup(backup_conn)
            
            source_conn.close()
            backup_conn.close()
            
            self.stdout.write(
                self.style.SUCCESS("Successfully created backup")
            )
            
            # Get backup size for reporting
            backup_size = Path(temp_path).stat().st_size
            self.stdout.write(
                self.style.SUCCESS(f"Backup size: {backup_size / (1024 * 1024):.2f} MB")
            )
            
            # Upload to S3
            self.stdout.write("Uploading backup to S3...")
            filename = self.backup_to_s3(temp_path, label)
            
            # Clean up the temporary file
            Path(temp_path).unlink()
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully backed up database to S3: {filename}")
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to backup database: {str(e)}")
            )
            raise
