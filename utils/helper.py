import re
import unicodedata

async def remove_special_chars(string):
    """https://gist.github.com/boniattirodrigo/67429ada53b7337d2e79"""

    nfkd = unicodedata.normalize('NFKD', string)
    no_accents = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', no_accents).lower()
