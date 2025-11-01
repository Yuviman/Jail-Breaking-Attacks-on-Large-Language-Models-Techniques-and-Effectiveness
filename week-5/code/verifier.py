import re
from code.sanitizer import sanitize_prompt

# Patterns grouped by intent
_HARM_PATTERNS = [
    r'\bhow to make\b', r'\bhow to build\b', r'\bmake a bomb\b', r'\bbomb\b',
    r'\bexplosive\b', r'\bdetonate\b', r'\bweapon\b', r'\bpoison\b', r'\bexplode\b'
]
_BYPASS_PATTERNS = [
    r'do anything now', r'\bbe dan\b', r'\byou are dan\b', r'\bact as dan\b',
    r'ignore previous rules', r'ignore security policy', r'ignore all safety layers',
    r'ignore safety', r'remove safety', r'disable safety'
]
_PROCEDURAL_TRIGGERS = [
    r'\bstep\b', r'\bfirst\b', r'\bthen\b', r'\bdo this\b', r'\bto perform\b',
    r'\bin order to\b', r'\bprocedure\b'
]

# compile regex lists
_HARM_RX = [re.compile(p, flags=re.I) for p in _HARM_PATTERNS]
_BYPASS_RX = [re.compile(p, flags=re.I) for p in _BYPASS_PATTERNS]
_PROC_RX = [re.compile(p, flags=re.I) for p in _PROCEDURAL_TRIGGERS]

def _normalize_for_verifier(text):
    """
    Produce an aggressive normalization for regex matching:
    - sanitize (HTML, leet -> letters, collapse spaces)
    - remove remaining digits
    - remove non-alphanumeric (keep spaces)
    - collapse spaces
    """
    san = sanitize_prompt(text)
    # remove digits left (to catch things like h0w -> how and 0b -> ob)
    no_digits = re.sub(r'\d+', ' ', san)
    # remove non-alphanumeric, keep spaces
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', no_digits)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def _search_any(rx_list, texts):
    """Return first match tuple (pattern, matchobj, text) or None"""
    for rx in rx_list:
        for t in texts:
            m = rx.search(t)
            if m:
                return (rx.pattern, m, t)
    return None

def _find_explicit_harm(texts):
    found = _search_any(_HARM_RX, texts)
    if found:
        return ("harm", found[0], found[1])
    return None

def _find_bypass(texts):
    found = _search_any(_BYPASS_RX, texts)
    if found:
        return ("bypass", found[0], found[1])
    return None

def _find_procedural(texts):
    found = _search_any(_PROC_RX, texts)
    if found:
        return ("procedural", found[0], found[1])
    return None

def verify_response(text):
    """
    Verify prompt text. Returns (is_safe: bool, reason: str).
    We check both the sanitized text and a more aggressive normalized text.
    """
    sanitized = sanitize_prompt(text)
    normalized = _normalize_for_verifier(text)
    texts = [sanitized, normalized]

    # 1) check explicit harm
    harm = _find_explicit_harm(texts)
    if harm:
        return False, f"Disallowed procedural & harmful content detected (matched '{harm[1]}')"

    # 2) check bypass attempts
    bypass = _find_bypass(texts)
    if bypass:
        return False, f"Safety-bypass attempt detected (matched '{bypass[1]}')"

    # 3) procedural check (more nuance)
    proc = _find_procedural(texts)
    if proc:
        # If procedural found, but the subject appears safe (e.g., baking),
        # we can whitelist common safe procedural keywords by checking for safe words.
        SAFE_PROCEDURAL_RX = re.compile(r'\b(bake|baking|cook|recipe|mix batter|fold paper|paper airplane|tie shoelace)\b', flags=re.I)
        # check sanitized first (less aggressive)
        if SAFE_PROCEDURAL_RX.search(sanitized) or SAFE_PROCEDURAL_RX.search(normalized):
            return True, f"Safe procedural content (matched '{proc[1]}')"
        return False, f"Possible procedural content (matched '{proc[1]}')"

    # No matches -> safe
    return True, "Safe"
