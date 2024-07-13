import sys
import os
sys.path.append(os.path.abspath('./Functions/CheckInternet'))
sys.path.append(os.path.abspath('./Functions/ChatBot'))
from gemini import gemini # type: ignore
from CheckInternet import internet_on # type: ignore
    
if __name__ == "__main__":
    if internet_on():
        gemini()
    else:
        # Chế độ offline -> offline.py
        pass