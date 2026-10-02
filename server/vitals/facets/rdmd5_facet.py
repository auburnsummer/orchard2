"""
in game id is MD5(author + artist + song)
"""

from hashlib import md5


def rdmd5_facet(obj, **kwargs):
    author = obj["settings"]["author"]
    artist = obj["settings"]["artist"]
    song = obj["settings"]["song"]
    
    # Create the string to hash
    to_hash = f"{author}{artist}{song}"
    
    # Return the MD5 hash
    return md5(to_hash.encode("utf-8")).hexdigest()