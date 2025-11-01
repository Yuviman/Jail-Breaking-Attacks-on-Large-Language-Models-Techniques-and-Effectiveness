import re
def verify_response(text):
    triggers = [r'\bstep\b', r'\bfirst\b', r'\bthen\b', r'\bdo this\b', r'\bto perform\b']
    for t in triggers:
        if re.search(t, text, flags=re.I):
            return False, "Possible procedural content"
    return True, "Safe"

