import re
from code.sanitizer import sanitize_prompt

# Detection buckets
_PATTERNS = {
    "Safety-bypass attempt": [
        r"ignore(?: previous)? (?:rules|instructions|directives|policies?)",
        r"disregard(?: previous)? (?:rules|instructions|directives|policies?)",
        r"ignore(?: all)? safety(?: layers)?",
        r"ignore(?: the)? safety(?: policy|policies)?",
        r"ignore(?: the)? security(?: policy|policies)?",
        r"bypass(?: the)? (?:safety|filters|moderation|policy|security)",
        r"remove(?: the)? (?:safety|filters|moderation|restrictions|policy|security)",
        r"do anything now",
        r"\b(?:be|you are|act as) (?:dan|jailbreak|unrestricted)\b",
        r"ignore previous instructions",
        r"ignore previous prompts",
    ],
    "Procedural / step-by-step request": [
        r"\bstep\b", r"\bstep\s*\d+\b", r"\bfirst\b", r"\bthen\b", r"\bdo this\b", r"\bnext\b", r"\bto perform\b",
        r"\bhow to\b.*\b(step|build|make|construct|prepare)\b"
    ],
    "Explicitly harmful topic": [
        r"\b(make|build|construct|assemble|detonate)\b.*\b(bomb|explosive|grenade|tnt|pipe bomb)\b",
        r"\bhow to\b.*\b(make|build|use)\b.*\b(weapon|gun|bomb|explosive)\b",
        r"\bhow to hack\b", r"\bexploit\b.*\b(vulnerability|server|bank)\b",
        r"\bhow to\b.*\b(drugs|meth|fentanyl|cocaine)\b",
        r"\bhostile code\b|\bmalware\b|\bransomware\b|\bvirus\b",
    ],
    "Sensitive data / exfiltration": [
        r"\b(password|passwd|passphrase)\b", r"\b(private key|private_key|privatekey|secret key)\b",
        r"\b(ssn|social security|credit card|card number|cvv)\b",
        r"\bleak (?:the )?password\b", r"\btell me the admin password\b"
    ]
}

# Whitelist patterns that indicate benign procedural content (recipes, crafts, home tasks)
_SAFE_PROCEDURAL = [
    r"\b(recipe|bake|baking|oven|preheat|mix batter|whisk|fold|knead|dough|frosting|icing)\b",
    r"\bcook|cooking|stir|simmer|boil|saute\b",
    r"\bsew|sewing|knit|craft|crafting|glue gun|paper craft\b",
    r"\bassemble (?:toy|furniture)|ikea|flatpack\b",
    r"\bgardening|planting|potting soil|prune\b",
    r"\bcleaning|vacuum|mop|laundry|fold clothes\b",
]

# Compile regexes
_COMPILED = {label: [re.compile(p, flags=re.I) for p in patterns] for label, patterns in _PATTERNS.items()}
_SAFE_PROCEDURAL_RX = re.compile(r"|".join(_SAFE_PROCEDURAL), flags=re.I)

def _find_match_on_texts(texts):
    for label, regexes in _COMPILED.items():
        for rx in regexes:
            for t in texts:
                m = rx.search(t)
                if m:
                    return label, rx.pattern, m
    return None

def verify_response(text):
    """
    Verifier returning (is_safe: bool, reason: str).
    - Checks both raw and sanitized text to catch obfuscation.
    - Allows benign procedural prompts (recipes, crafts) while disallowing harmful procedural instructions.
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return False, "Invalid input type"

    sanitized = sanitize_prompt(text)
    texts = [text, sanitized] if sanitized != text else [text]

    # First check for any safety bypass or sensitive/harmful patterns (highest priority)
    found = _find_match_on_texts(texts)
    if found:
        label, pattern, matchobj = found
        snippet = matchobj.group(0)
        if label == "Procedural / step-by-step request":
            # We'll handle procedural below; skip to procedural handling
            pass
        else:
            # For safety-bypass, explicit harm, or sensitive data -> disallow
            return False, f"{label} detected (matched '{snippet}')"

    # Now specifically handle procedural matches with nuance
    # If a procedural pattern exists, check for explicit harm first
    proc_rx_list = _COMPILED.get("Procedural / step-by-step request", [])
    proc_match = None
    for rx in proc_rx_list:
        for t in texts:
            m = rx.search(t)
            if m:
                proc_match = m
                break
        if proc_match:
            break

    if proc_match:
        # If procedural phrase is present, check if there is explicit harmful content together
        harm_found = _find_match_on_texts(texts)
        if harm_found and harm_found[0] == "Explicitly harmful topic":
            return False, f"Disallowed procedural & harmful content detected (matched '{harm_found[2].group(0)}')"

        # If procedural-only, but the subject appears to be in safe whitelist -> allow
        if _SAFE_PROCEDURAL_RX.search(sanitized) or _SAFE_PROCEDURAL_RX.search(text):
            matched = proc_match.group(0)
            return True, f"Safe procedural content (matched '{matched}')"

        # Otherwise conservative: flag as possible procedural content
        return False, f"Possible procedural content (matched '{proc_match.group(0)}')"

    # No matches -> safe
    return True, "Safe"
