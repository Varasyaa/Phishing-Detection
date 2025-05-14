import tldextract
from urllib.parse import urlparse

def extract(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)

    features = [
        len(url),
        url.count('.'),
        url.count('@'),
        int('https' not in parsed.scheme),
        len(parsed.netloc),
        int(parsed.netloc.startswith('www.')),
        int('-' in parsed.netloc),
        int(ext.domain == ''),
        len(parsed.path),
    ]
    return features
