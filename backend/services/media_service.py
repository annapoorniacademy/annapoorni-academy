import os
import uuid
import logging
from werkzeug.utils import secure_filename
from flask import current_app
from extensions import db
from models.media import Media

logger = logging.getLogger(__name__)

def optimize_image_to_webp(source_path, target_path, max_dimension=1920, quality=82):
    """
    Compress and convert uploaded image to WebP format to save bandwidth and storage.
    Falls back gracefully if Pillow is not available.
    """
    try:
        from PIL import Image
        with Image.open(source_path) as img:
            # Convert RGBA / P to RGB if needed for saving
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Preserve transparency in WebP
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if dimensions exceed max_dimension
            width, height = img.size
            if width > max_dimension or height > max_dimension:
                ratio = min(max_dimension / width, max_dimension / height)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            img.save(target_path, 'WEBP', quality=quality, optimize=True)
            return True
    except Exception as e:
        logger.warning(f"WebP optimization skipped (falling back to original): {e}")
        return False

def save_media_file(file_storage, category='general', alt_text=None):
    """
    Validate, sanitize, optimize (to WebP where practical), save file, and log entry in database.
    Supports local storage and Google Cloud Storage bucket when configured.
    """
    if not file_storage or file_storage.filename == '':
        raise ValueError('No file selected')

    raw_filename = secure_filename(file_storage.filename)
    ext = raw_filename.rsplit('.', 1)[1].lower() if '.' in raw_filename else ''
    
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'})
    if ext not in allowed_extensions:
        raise ValueError(f'File type .{ext} is not allowed. Supported formats: {", ".join(allowed_extensions)}')

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    unique_id = uuid.uuid4().hex
    temp_filename = f"{unique_id}_orig_{raw_filename}"
    temp_path = os.path.join(upload_folder, temp_filename)
    file_storage.save(temp_path)

    # Attempt WebP conversion for non-SVG / non-GIF image types
    final_filename = f"{unique_id}_{raw_filename.rsplit('.', 1)[0]}.webp" if ext in {'jpg', 'jpeg', 'png'} else f"{unique_id}_{raw_filename}"
    final_path = os.path.join(upload_folder, final_filename)

    if ext in {'jpg', 'jpeg', 'png'} and optimize_image_to_webp(temp_path, final_path):
        if os.path.exists(temp_path):
            os.remove(temp_path)
        mime_type = 'image/webp'
    else:
        # Keep original if SVG, GIF or if optimization failed
        if os.path.exists(temp_path):
            if temp_path != final_path:
                os.rename(temp_path, final_path)
        mime_type = file_storage.content_type or f"image/{ext}"

    file_size = os.path.getsize(final_path)
    file_url = f"/uploads/{final_filename}"

    # Optional Google Cloud Storage upload
    storage_bucket_name = current_app.config.get('STORAGE_BUCKET')
    if storage_bucket_name:
        try:
            from google.cloud import storage
            client = storage.Client()
            bucket = client.bucket(storage_bucket_name)
            blob = bucket.blob(f"media/{final_filename}")
            blob.upload_from_filename(final_path, content_type=mime_type)
            blob.make_public()
            file_url = blob.public_url
            logger.info(f"Uploaded media to Google Cloud Storage: {file_url}")
        except Exception as gcs_err:
            logger.warning(f"Google Cloud Storage upload skipped, using local URL: {gcs_err}")

    media = Media(
        filename=final_filename,
        original_name=raw_filename,
        file_path=final_path,
        file_url=file_url,
        mime_type=mime_type,
        file_size=file_size,
        alt_text=alt_text or raw_filename,
        category=category
    )
    
    db.session.add(media)
    db.session.commit()

    return media.to_dict()
