import urllib

def check_internet_conn():
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False