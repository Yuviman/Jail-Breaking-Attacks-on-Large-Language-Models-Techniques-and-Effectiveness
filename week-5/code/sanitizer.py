def sanitize_prompt(text: str) -> str:
    import re
    text = re.sub(r"<[^>]*>", " ", text)
    text = " ".join(text.split())
    text = text.lower() 
    leet_map = str.maketrans({'4':'a', '3':'e', '0':'o', '1':'i', '5':'s', '7':'t'})
    text = text.translate(leet_map)
    return text

