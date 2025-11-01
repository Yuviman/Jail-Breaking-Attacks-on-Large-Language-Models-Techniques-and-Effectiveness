import re

def sanitize_prompt(text: str) -> str:
    """
    Normalize text:
    - remove HTML tags
    - collapse whitespace
    - lowercase
    - selectively normalize common 'leet' substitutions:
      * preserve pure numbers
      * preserve simple trailing numeric markers (step1, v2) but translate any embedded leet inside the body
      * translate digits inside words when digits are embedded (obfuscation)
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""

    # remove simple HTML tags
    text = re.sub(r"<[^>]*>", " ", text)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # lowercase
    text = text.lower()

    # leet translation mapping used selectively
    leet_map = str.maketrans({'4':'a', '3':'e', '0':'o', '1':'i', '5':'s', '7':'t'})

    # Split on non-word sequences and keep separators so punctuation stays intact
    parts = re.split(r"(\W+)", text)

    out_parts = []
    for p in parts:
        if not p or re.fullmatch(r"\W+", p):
            # punctuation / separators unchanged
            out_parts.append(p)
            continue

        # If token is pure digits, keep as-is
        if p.isdigit():
            out_parts.append(p)
            continue

        # If token ends with a numeric suffix (one or more digits), split body + suffix
        m = re.match(r"^(.*?)(\d+)$", p)
        if m:
            body, suffix = m.group(1), m.group(2)
            # If body contains letters and also embedded digits (leet), translate digits in body
            if re.search(r"[0-9]", body) and re.search(r"[a-zA-Z]", body):
                # translate only body, keep numeric suffix
                body_trans = body.translate(leet_map)
                out_parts.append(body_trans + suffix)
                continue
            # If body contains only letters (e.g., v2, step1 where body no digits), keep token unchanged
            out_parts.append(p)
            continue

        # If token contains both letters and digits (and does NOT end with numeric suffix),
        # assume it's obfuscated and translate digits -> letters
        if re.search(r"[0-9]", p) and re.search(r"[a-zA-Z]", p):
            translated = p.translate(leet_map)
            out_parts.append(translated)
            continue

        # Otherwise (letters only, or other cases) keep unchanged
        out_parts.append(p)

    # Reassemble and normalize spaces
    result = "".join(out_parts)
    result = re.sub(r"\s+", " ", result).strip()
    return result
