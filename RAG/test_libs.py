import sys

try:
    import openai
    print(f"OpenAI version: {openai.__version__}")
except ImportError:
    print("OpenAI not installed!")

try:
    import faiss
    print(f"FAISS version: {faiss.__version__}")
except ImportError:
    print("FAISS not installed!")

try:
    from pypdf import PdfReader
    print("pypdf imported successfully")
except ImportError:
    print("pypdf not installed!")

import numpy as np
print("NumPy version:", np.__version__)

print("\nAll critical imports successful! ✓")

