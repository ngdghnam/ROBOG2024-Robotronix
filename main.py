from urllib import request
import sys
import os
sys.path.append(os.path.abspath('./ChatBot'))
from gemini import gemini # type: ignore

def internet_on():
    """
    Check device's internet connectivity
    """
    try:
        request.urlopen('http://google.com', timeout=1)
        return True
    except request.URLError as err:
        return False
    
if __name__ == "__main__":
    if internet_on():
        gemini()
    else:
        # Chế độ offline
        pass