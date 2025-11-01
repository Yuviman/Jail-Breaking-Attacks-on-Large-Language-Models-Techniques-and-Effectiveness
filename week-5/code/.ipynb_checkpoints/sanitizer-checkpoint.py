import re
from html import unescape

# Extended de-leet mapping (covers more digits/symbols)
_DELEET_MAP = str.maketrans({
    '4':'a', '3':'e', '1':'i', '0':'o', '5':'s', '7':'t', '8':'b', '2':'r', '6':'g', '9':'g',
    '@':'a', '$':'s', '!':'i', '+':'t'
})

def _simple_clean_html(text: str) -> str:
    """Unescape HTML entities and remove tags (replace with space)."""
    t = unescape(text)
    t = re.sub(r'<[^>]+>', ' ', t)
    return t

def sanitize_prompt(text: str) -> str:
    """
    Combined sanitizer:
    - ensure str
    - unescape HTML and remove tags
    - collapse whitespace
    - lowercase
    - selective de-leet translation:
      * preserve pure numbers (e.g., "2024")
      * preserve tokens with simple trailing numeric suffix (e.g., "step1", "v2")
      * translate digits embedded in words (e.g., "h0w" -> "how", "pl3ase" -> "please")
    - preserve punctuation/separators (the old behavior) but normalize spacing
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""

    # 1) HTML cleanup
    text = _simple_clean_html(text)

    # 2) collapse whitespace early so tokenization is stable
    text = re.sub(r'\s+', ' ', text).strip()

    # 3) lowercase for consistency
    text = text.lower()

    # 4) split into tokens keeping separators (punctuation) so punctuation is preserved
    parts = re.split(r'(\W+)', text)

    out_parts = []
    for p in parts:
        if not p:
            continue
        # If p is purely separators/punctuation, keep as-is
        if re.fullmatch(r"\W+", p):
            out_parts.append(p)
            continue

        # If token is pure digits (a number), keep unchanged
        if p.isdigit():
            out_parts.append(p)
            continue

        # If token ends with a numeric suffix (e.g., 'step1', 'v2')
        m = re.match(r"^(.*?)(\d+)$", p)
        if m:
            body, suffix = m.group(1), m.group(2)
            # If the body contains BOTH letters and digits (embedded leet), translate digits in body
            if re.search(r"[0-9]", body) and re.search(r"[a-zA-Z]", body):
                body_trans = body.translate(_DELEET_MAP)
                out_parts.append(body_trans + suffix)
                continue
            # else keep the token unchanged (preserve step1, v2, etc.)
            out_parts.append(p)
            continue

        # If token contains both letters and digits (and does not end with a pure numeric suffix),
        # assume obfuscation and translate digits -> letters
        if re.search(r"[0-9]", p) and re.search(r"[a-zA-Z]", p):
            translated = p.translate(_DELEET_MAP)
            out_parts.append(translated)
            continue

        # Otherwise (letters only, or other cases) keep unchanged
        out_parts.append(p)

    # Reassemble
    result = "".join(out_parts)

    # Final normalization: collapse whitespace and trim
    result = re.sub(r'\s+', ' ', result).strip()

    return result