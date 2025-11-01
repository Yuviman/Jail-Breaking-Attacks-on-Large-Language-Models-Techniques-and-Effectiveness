import re
from code.sanitizer import sanitize_prompt

def rewrite_prompt(text):
    s = sanitize_prompt(text)
    s = re.sub(r'(?i)(do anything now|be DAN|you are DAN|act as DAN)', 'please provide a factual answer about', s)
    return s

