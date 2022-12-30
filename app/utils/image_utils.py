import base64
from io import BytesIO

import boto3
from PIL import Image, UnidentifiedImageError

from config import get_env


def get_image_size(image):
    try:
        image = Image.open(BytesIO(base64.b64decode(image)))
    except UnidentifiedImageError:
        raise ValueError("Invalid Image")
    return image.size


def resize_image(image, size):
    image = Image.open(BytesIO(base64.b64decode(image)))
    width, height = image.size
    ratio = width / height
    image = image.resize((size, int(size / ratio)))
    buffered = BytesIO()
    image.save(buffered, format="WEBP")
    return image, len(buffered.getvalue())


def get_squared_thumbnail(image):
    image = Image.open(BytesIO(base64.b64decode(image)))
    width, height = image.size
    if width > height:
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
        image = image.crop((int(left), int(top), int(right), int(bottom)))
    elif width < height:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = (height + width) / 2
        image = image.crop((int(left), int(top), int(right), int(bottom)))
    image = image.resize((200, 200))
    buffered = BytesIO()
    image.save(buffered, format="WEBP")
    return image, len(buffered.getvalue())


def get_image_extension(image):
    image = Image.open(BytesIO(base64.b64decode(image)))
    return image.format


def get_image_mime(image):
    image = Image.open(BytesIO(base64.b64decode(image)))
    return image.format.lower()


def get_image_file_size(image):
    image = Image.open(BytesIO(base64.b64decode(image)))
    buffered = BytesIO()
    image.save(buffered)
    return len(buffered.getvalue())


def s3_upload(image, file_name):
    conf = get_env()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=conf.AWS_ACCESS_KEY,
        aws_secret_access_key=conf.AWS_SECRET_KEY,
        region_name=conf.AWS_REGION,
    )
    buffered = BytesIO()
    image.save(buffered, format="WEBP")
    s3.put_object(
        Bucket=conf.AWS_BUCKET_NAME,
        Key=f"{file_name}",
        Body=buffered.getvalue(),
        ACL="public-read",
        ContentType="image/webp",
    )
    return f"https://{conf.AWS_BUCKET_NAME}.s3.{conf.AWS_REGION}.amazonaws.com/{file_name}"
