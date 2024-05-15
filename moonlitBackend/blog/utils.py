import re, os, random, string, time
from django.conf import settings

def generate_random_name(length=10):
    """Generate a random name for an image."""
    timestamp = str(int(time.time()))  # Use timestamp to ensure uniqueness
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    random_name = f"{timestamp}_{random_string}"
    return random_name


def extract_base64_images(html_content):
    # Use regex to find all base64-encoded image data in the HTML content
    base64_images = re.findall(r'data:image\/\w+;base64,([^\'\"\r\n]+)', html_content)
    print(base64_images)
    return base64_images

def replace_base64_with_urls(content, base64_string, image_url):
    # Escape special characters in the base64 string
    escaped_base64 = re.escape(base64_string)

    # Construct the pattern to match img tags with src attribute containing the base64 string
    pattern = rf'<img[^>]*src\s*=\s*["\'](data:image/[^;]+;base64,{escaped_base64})["\'][^>]*>'

    # Replace matching img tags with the provided image URL
    replaced_content = re.sub(pattern, f'<img src="{image_url}">', content)

    return replaced_content


def get_image_url(image_name):
    return f"{settings.ABSOLUTE_URL}/media/{image_name.image.name}"