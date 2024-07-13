from urllib import request

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
    print(internet_on())