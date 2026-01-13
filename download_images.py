#!/usr/bin/env python3
"""
Phase 3: Download reference images for BJJ techniques
Reads download_urls.txt files and downloads images from reference sites.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
import ssl

# Create SSL context that doesn't verify certificates (for some sites)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class ImageExtractor(HTMLParser):
    """Extract image URLs from HTML."""
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            src = attrs_dict.get('src') or attrs_dict.get('data-src') or attrs_dict.get('data-lazy-src')
            if src:
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    parsed = urllib.parse.urlparse(self.base_url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                elif not src.startswith('http'):
                    src = urllib.parse.urljoin(self.base_url, src)
                self.images.append(src)

def get_headers():
    """Return headers to mimic a browser request."""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

def fetch_page(url, timeout=15):
    """Fetch a webpage and return its HTML content."""
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None

def extract_images_from_html(html, base_url):
    """Extract image URLs from HTML content."""
    parser = ImageExtractor(base_url)
    try:
        parser.feed(html)
    except:
        pass
    return parser.images

def filter_good_images(image_urls, technique_name):
    """Filter images to find relevant BJJ technique images."""
    good_images = []
    technique_lower = technique_name.lower().replace('_', ' ').replace('-', ' ')

    # Keywords to avoid
    negative_keywords = ['logo', 'icon', 'avatar', 'banner', 'ad', 'advertisement',
                        'facebook', 'twitter', 'instagram', 'pinterest', 'share',
                        'arrow', 'button', 'menu', 'nav', 'footer', 'header',
                        'gravatar', 'emoji', 'smiley', 'pixel', '1x1', 'spacer',
                        'spinner', 'loading', 'placeholder']

    for url in image_urls:
        url_lower = url.lower()

        # Skip small images and icons
        if any(neg in url_lower for neg in negative_keywords):
            continue

        # Skip data URLs and SVGs
        if url.startswith('data:') or url.endswith('.svg'):
            continue

        # Skip very short URLs (likely icons)
        if len(url) < 30:
            continue

        # Check for image extensions
        if not any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            # Some URLs don't have extensions but are images
            if 'image' not in url_lower and 'photo' not in url_lower:
                continue

        # Prefer larger images (URLs often contain size info)
        size_match = re.search(r'(\d+)x(\d+)', url)
        if size_match:
            w, h = int(size_match.group(1)), int(size_match.group(2))
            if w < 200 or h < 200:
                continue

        good_images.append(url)

    return good_images

def download_image(url, filepath, timeout=20):
    """Download an image to the specified filepath."""
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            content = response.read()

            # Verify it's actually an image (check magic bytes)
            if content[:2] == b'\xff\xd8':  # JPEG
                ext = '.jpg'
            elif content[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
                ext = '.png'
            elif content[:6] in (b'GIF87a', b'GIF89a'):  # GIF
                ext = '.gif'
            elif content[:4] == b'RIFF' and content[8:12] == b'WEBP':  # WebP
                ext = '.webp'
            else:
                # Try to save anyway
                ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or '.jpg'

            # Update filepath with correct extension
            filepath = os.path.splitext(filepath)[0] + ext

            with open(filepath, 'wb') as f:
                f.write(content)

            # Check file size (skip if too small - likely an icon)
            if os.path.getsize(filepath) < 5000:  # Less than 5KB
                os.remove(filepath)
                return None

            return filepath
    except Exception as e:
        print(f"    Error downloading {url}: {e}")
        return None

def is_search_url(url):
    """Check if URL is a search engine URL (skip these)."""
    search_patterns = [
        'google.com/search',
        'bing.com/images',
        'youtube.com/results',
        'duckduckgo.com',
    ]
    return any(pattern in url.lower() for pattern in search_patterns)

def is_reference_site(url):
    """Check if URL is from a known BJJ reference site."""
    reference_domains = [
        'bjjheroes.com',
        'grapplearts.com',
        'evolve-mma.com',
        'bjjfanatics.com',
        'submissionsearcher.com',
        'bjj.university',
        'bjjequipment.com',
        'wikipedia.org',
        'wikimedia.org',
        'infighting.ca',
        'bjjsportswear.com',
        'bjjgraph.org',
    ]
    return any(domain in url.lower() for domain in reference_domains)

def process_technique_folder(folder_path):
    """Process a single technique folder and download images."""
    urls_file = os.path.join(folder_path, 'download_urls.txt')
    images_dir = os.path.join(folder_path, 'images')

    if not os.path.exists(urls_file):
        return 0

    # Check if images already downloaded
    if os.path.exists(images_dir) and len(os.listdir(images_dir)) >= 3:
        return len(os.listdir(images_dir))

    # Create images directory
    os.makedirs(images_dir, exist_ok=True)

    technique_name = os.path.basename(folder_path)
    print(f"\nProcessing: {technique_name}")

    # Read URLs
    with open(urls_file, 'r') as f:
        content = f.read()

    # Extract URLs (skip comments and empty lines)
    urls = []
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('==='):
            if line.startswith('http'):
                urls.append(line)

    # Collect all potential images
    all_images = []

    for url in urls:
        # Skip search engine URLs
        if is_search_url(url):
            continue

        # Only process reference sites
        if not is_reference_site(url):
            continue

        print(f"  Fetching: {url[:60]}...")
        html = fetch_page(url)
        if html:
            images = extract_images_from_html(html, url)
            filtered = filter_good_images(images, technique_name)
            all_images.extend(filtered)
            time.sleep(0.5)  # Be polite to servers

    # Remove duplicates while preserving order
    seen = set()
    unique_images = []
    for img in all_images:
        if img not in seen:
            seen.add(img)
            unique_images.append(img)

    # Download up to 5 images
    downloaded = 0
    for i, img_url in enumerate(unique_images[:10]):  # Try up to 10, keep 5
        if downloaded >= 5:
            break

        filepath = os.path.join(images_dir, f"{downloaded + 1:02d}.jpg")
        print(f"  Downloading: {img_url[:60]}...")
        result = download_image(img_url, filepath)
        if result:
            downloaded += 1
            print(f"    Saved: {os.path.basename(result)}")
        time.sleep(0.3)

    print(f"  Downloaded {downloaded} images")
    return downloaded

def main():
    """Main function to process all technique folders."""
    base_dir = Path(__file__).parent

    categories = ['positions', 'submissions', 'sweeps', 'passes', 'takedowns', 'escapes', 'transitions']

    # Allow filtering by category from command line
    if len(sys.argv) > 1:
        categories = [c for c in categories if c in sys.argv[1:]]

    total_downloaded = 0
    total_folders = 0

    for category in categories:
        category_dir = base_dir / category
        if not category_dir.exists():
            continue

        print(f"\n{'='*60}")
        print(f"Category: {category.upper()}")
        print('='*60)

        for technique_dir in sorted(category_dir.iterdir()):
            if technique_dir.is_dir():
                total_folders += 1
                downloaded = process_technique_folder(str(technique_dir))
                total_downloaded += downloaded

    print(f"\n{'='*60}")
    print(f"COMPLETE: Downloaded {total_downloaded} images across {total_folders} folders")
    print('='*60)

if __name__ == '__main__':
    main()
