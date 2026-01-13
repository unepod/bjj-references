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

def fetch_page(url, timeout=8):
    """Fetch a webpage and return its HTML content."""
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    Error: {e}", flush=True)
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
    negative_keywords = ['logo', 'icon', 'avatar', 'banner', 'ad-', '/ads/',
                        'facebook', 'twitter', 'instagram', 'pinterest', 'share',
                        'arrow', 'button', 'menu', 'nav-', 'footer', 'header',
                        'gravatar', 'emoji', 'smiley', 'pixel', '1x1', 'spacer',
                        'spinner', 'loading', 'placeholder', 'thumbnail-small',
                        'author', 'profile', 'user-', 'comment']

    for url in image_urls:
        url_lower = url.lower()

        # Skip small images and icons
        if any(neg in url_lower for neg in negative_keywords):
            continue

        # Skip data URLs and SVGs
        if url.startswith('data:') or url.endswith('.svg'):
            continue

        # Skip very short URLs (likely icons)
        if len(url) < 20:
            continue

        # Check for image extensions or common image URL patterns
        has_extension = any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif'])
        has_image_path = any(pattern in url_lower for pattern in ['upload', 'image', 'photo', 'media', 'thumb', 'wp-content'])

        if not has_extension and not has_image_path:
            continue

        # Prefer larger images (URLs often contain size info)
        size_match = re.search(r'(\d+)x(\d+)', url)
        if size_match:
            w, h = int(size_match.group(1)), int(size_match.group(2))
            if w < 150 or h < 150:
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

def search_technique_images(technique_name):
    """Search for technique images using DuckDuckGo."""
    # Build search URLs for technique-specific pages
    search_term = technique_name.replace('_', ' ')

    # DuckDuckGo image search (returns HTML with image URLs)
    ddg_url = f"https://duckduckgo.com/?q={urllib.parse.quote(search_term + ' BJJ')}&iax=images&ia=images"

    # Try to get images from specific BJJ sites
    site_searches = [
        f"https://www.bjjheroes.com/?s={urllib.parse.quote(search_term)}",
        f"https://www.grapplearts.com/?s={urllib.parse.quote(search_term)}",
        f"https://evolve-mma.com/?s={urllib.parse.quote(search_term)}",
    ]

    return site_searches

def download_direct_image(url, filepath, timeout=20):
    """Download an image directly from a URL."""
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            content_type = response.headers.get('Content-Type', '')
            content = response.read()

            # Determine extension from content
            if content[:2] == b'\xff\xd8':
                ext = '.jpg'
            elif content[:8] == b'\x89PNG\r\n\x1a\n':
                ext = '.png'
            elif content[:6] in (b'GIF87a', b'GIF89a'):
                ext = '.gif'
            elif content[:4] == b'RIFF' and len(content) > 12 and content[8:12] == b'WEBP':
                ext = '.webp'
            else:
                ext = '.jpg'

            filepath = os.path.splitext(filepath)[0] + ext

            with open(filepath, 'wb') as f:
                f.write(content)

            if os.path.getsize(filepath) < 5000:
                os.remove(filepath)
                return None

            return filepath
    except Exception as e:
        print(f"    Error: {e}")
        return None

def process_technique_folder(folder_path):
    """Process a single technique folder and download images."""
    urls_file = os.path.join(folder_path, 'download_urls.txt')
    images_dir = os.path.join(folder_path, 'images')

    if not os.path.exists(urls_file):
        return 0

    # Check if images already downloaded
    if os.path.exists(images_dir) and len(os.listdir(images_dir)) >= 3:
        print(f"  Skipping {os.path.basename(folder_path)} (already has images)")
        return len(os.listdir(images_dir))

    # Create images directory
    os.makedirs(images_dir, exist_ok=True)

    technique_name = os.path.basename(folder_path)
    search_term = technique_name.replace('_', ' ')
    print(f"\nProcessing: {technique_name}", flush=True)

    # Collect all potential images
    all_images = []

    # Build various search terms
    search_variations = [search_term]
    # Add "BJJ" suffix for common terms
    if not any(w in search_term.lower() for w in ['bjj', 'jiu', 'jitsu']):
        search_variations.append(search_term + ' BJJ')

    # Strategy 1: Search BJJ sites directly for this technique
    search_urls = []
    for term in search_variations:
        search_urls.extend([
            f"https://www.bjjheroes.com/?s={urllib.parse.quote(term)}",
            f"https://evolve-mma.com/?s={urllib.parse.quote(term)}",
        ])

    # Add Wikipedia for known technique names (mapped)
    wiki_mappings = {
        'mount': 'Mount_(grappling)',
        'mount_top': 'Mount_(grappling)',
        'mount_bottom': 'Mount_(grappling)',
        'side_control': 'Side_control',
        'side_control_top': 'Side_control',
        'side_control_bottom': 'Side_control',
        'closed_guard': 'Guard_(grappling)#Closed_guard',
        'closed_guard_top': 'Guard_(grappling)#Closed_guard',
        'closed_guard_bottom': 'Guard_(grappling)#Closed_guard',
        'half_guard': 'Half_guard',
        'half_guard_top': 'Half_guard',
        'half_guard_bottom': 'Half_guard',
        'back_control': 'Back_mount',
        'back_top': 'Back_mount',
        'armbar': 'Armlock',
        'arm_bar': 'Armlock',
        'triangle': 'Triangle_choke',
        'triangle_choke': 'Triangle_choke',
        'kimura': 'Kimura_lock',
        'americana': 'Americana_(grappling)',
        'guillotine': 'Guillotine_choke',
        'guillotine_choke': 'Guillotine_choke',
        'rear_naked_choke': 'Rear_naked_choke',
        'rnc': 'Rear_naked_choke',
        'omoplata': 'Omoplata',
        'knee_on_belly': 'Knee-on-stomach',
        'north_south': 'North-south_position',
        'turtle': 'Turtle_(grappling)',
        'butterfly_guard': 'Butterfly_guard',
        'ashi_garami': 'Ashi_garami',
        'de_la_riva': 'De_la_Riva_guard',
    }
    wiki_key = technique_name.lower()
    if wiki_key in wiki_mappings:
        search_urls.append(f"https://en.wikipedia.org/wiki/{wiki_mappings[wiki_key]}")

    # Strategy 1a: Try direct article URLs first (faster, more reliable)
    direct_urls = search_evolve_technique(technique_name)
    for url in direct_urls:
        print(f"  Trying direct: {url[:55]}...")
        html = fetch_page(url)
        if html and '<article' in html.lower():  # Verify it's an actual article
            images = extract_images_from_html(html, url)
            filtered = filter_good_images(images, technique_name)
            # Prioritize images that might be technique-related
            for img in filtered:
                img_lower = img.lower()
                if any(w in img_lower for w in search_term.lower().split() if len(w) > 3):
                    all_images.insert(0, img)  # Add to front
                else:
                    all_images.append(img)
            if len(all_images) >= 5:
                break
        time.sleep(0.1)

    # Strategy 1b: Search pages if we need more images
    if len(all_images) < 5:
        for url in search_urls:
            print(f"  Searching: {url[:60]}...", flush=True)
            html = fetch_page(url)
            if html:
                # First, look for article links in search results
                article_urls = extract_article_links(html, url, search_term)
                for article_url in article_urls[:2]:  # Check first 2 articles
                    print(f"    Found article: {article_url[:50]}...", flush=True)
                    article_html = fetch_page(article_url)
                    if article_html:
                        images = extract_images_from_html(article_html, article_url)
                        filtered = filter_good_images(images, technique_name)
                        all_images.extend(filtered)
                    time.sleep(0.1)
            time.sleep(0.2)
            if len(all_images) >= 10:
                break

    # Strategy 2: Also check URLs from download_urls.txt (if any are direct image URLs)
    with open(urls_file, 'r') as f:
        content = f.read()

    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('http') and any(ext in line.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            all_images.append(line)

    # Remove duplicates while preserving order
    seen = set()
    unique_images = []
    for img in all_images:
        if img not in seen:
            seen.add(img)
            unique_images.append(img)

    print(f"  Found {len(unique_images)} potential images", flush=True)

    # Download up to 5 images
    downloaded = 0
    for i, img_url in enumerate(unique_images[:15]):  # Try up to 15, keep 5
        if downloaded >= 5:
            break

        filepath = os.path.join(images_dir, f"{downloaded + 1:02d}.jpg")
        result = download_image(img_url, filepath)
        if result:
            downloaded += 1
            print(f"    Saved: {os.path.basename(result)}", flush=True)
        time.sleep(0.1)

    print(f"  Downloaded {downloaded} images", flush=True)
    return downloaded


def extract_article_links(html, base_url, search_term):
    """Extract article links from search results that match the technique."""
    links = []
    search_words = [w for w in search_term.lower().split() if len(w) > 2]

    # Simple regex to find article links
    href_pattern = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

    for match in href_pattern.finditer(html):
        href = match.group(1)

        # Convert relative URLs
        if href.startswith('/'):
            parsed = urllib.parse.urlparse(base_url)
            href = f"{parsed.scheme}://{parsed.netloc}{href}"
        elif not href.startswith('http'):
            continue

        href_lower = href.lower()

        # Skip non-article URLs
        skip_patterns = ['#', 'javascript:', 'mailto:', 'wp-content', 'wp-includes',
                         'category/', 'tag/', 'author/', 'page=', 'login', 'cart',
                         'facebook.com', 'twitter.com', 'instagram.com', 'youtube.com',
                         '/feed/', 'comment', 'reply', 'search', '?s=', 'cdn.']
        if any(skip in href_lower for skip in skip_patterns):
            continue

        # Check if URL contains technique-related words
        matches = sum(1 for word in search_words if word in href_lower)
        if matches > 0:
            links.append((matches, href))

    # Sort by number of matches (descending) and return top 5
    links.sort(key=lambda x: x[0], reverse=True)
    return [href for _, href in links[:5]]


def search_evolve_technique(technique_name):
    """Search Evolve MMA for technique-specific articles."""
    search_term = technique_name.replace('_', '-')
    # Evolve MMA has a predictable URL pattern for BJJ content
    urls = [
        f"https://evolve-mma.com/blog/{search_term}/",
        f"https://evolve-mma.com/blog/{search_term}-bjj/",
        f"https://evolve-mma.com/blog/how-to-do-the-{search_term}/",
        f"https://evolve-mma.com/blog/the-{search_term}/",
    ]
    return urls

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
