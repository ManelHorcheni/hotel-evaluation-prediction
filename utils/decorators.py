import time
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"⏱️ Démarrage '{func.__name__}'...")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"✅ Terminé '{func.__name__}' en {end - start:.2f} secondes.")
        return result
    return wrapper
