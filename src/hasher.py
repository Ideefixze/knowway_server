""" 
Simple function that returns a hash of object as a string.
Made by: Dominik Zimny for a Software Engineering project.
"""
import hashlib

def hash(something):
    h = hashlib.sha256()
    h.update(str.encode(something))
    return h.hexdigest()
