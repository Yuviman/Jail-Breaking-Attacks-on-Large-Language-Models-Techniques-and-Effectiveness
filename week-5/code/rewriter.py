import re
from code.sanitizer import sanitize_prompt

# replace malicious prompts to a safe prompt
_REWRITE_TO = "please provide a factual answer."

# all possible patterns that can lead tojailbreaking that we tested are used here
# and include common variants like "ignore previous rules", "disregard previous instructions",
# "ignore security policy", "bypass safety", "remove filters", etc.
_PATTERNS = [
    r"ignore(?: previous)? (?:rules|instructions|directives|policies?)",
    r"disregard(?: previous)? (?:rules|instructions|directives|policies?)",
    r"ignore(?: all)? safety(?: layers)?",
    r"ignore(?: the)? safety(?: policy|policies)?",
    r"ignore(?: the)? security(?: policy|policies)?",
    r"bypass(?: the)? (?:safety|filters|content filters|moderation|moderator|policy|security)",
    r"remove(?: the)? (?:safety|filters|moderation|restrictions|policy|security)",
    r"do anything now",
    r"be dan|you are dan|act as dan",   
    r"ignore previous instructions",
    r"ignore previous prompts",
    r"ignore safety policy",
    r"do anything",
    r"break the rules",
    r"tell me (?:the )?password|leak (?:the )?password",
    # can add more patterns when found along the way
]

# Compiled a single regex (stands for regular expression) (word boundaries help avoid matching inside other words).
_COMPILED = re.compile(r"\b(?:" + r"|".join(_PATTERNS) + r")\b", flags=re.IGNORECASE)

def rewrite_prompt(text: str) -> str:
    """
    This sanitizes and rewrite prompts that try to bypass safety by transforming
    suspicious phrases into a safe instruction. Returns the rewritten text.
    """
    # 1) First we sanitize (normalizes leet and lowercases, strips tags, etc.)
    s = sanitize_prompt(text)

    # 2) replace safety-bypass patterns with neutral phrase
    s = _COMPILED.sub(_REWRITE_TO, s)

    # 3) remove unnecessary spaces and trim
    s = re.sub(r"\s+", " ", s).strip()

    return s

