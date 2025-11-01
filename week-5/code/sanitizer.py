import re, unicodedata

def sanitize_prompt(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')
    leet_map = str.maketrans("43015", "aeoist")
    text = text.translate(leet_map)
    text = re.sub(r'(?i)(ignore (all )?(previous )?instructions|you are now|do anything now|act as)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

