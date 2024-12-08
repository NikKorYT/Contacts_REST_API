import cloudinary
import cloudinary.uploader
from config.general import settings

def init_cloudinary():
    try:
        cloudinary.config(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )
    except Exception as e:
        print(f"Cloudinary config error: {str(e)}")
        raise

async def upload_avatar(file, user_id: int) -> str:
    try:
        r = cloudinary.uploader.upload(
            file,
            public_id=f'users/avatars/{user_id}',
            overwrite=True,
            transformation={
                'width': 250,
                'height': 250,
                'crop': 'fill',
                'gravity': 'face'
            }
        )
        return r.get('secure_url')
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise