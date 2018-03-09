import urllib.request as rq
import re
from datetime import datetime

def get_domain_age(url):
    response = rq.urlopen("https://www.whois.com/whois/"+url)

    html = response.read().decode("utf-8")
    match = re.search("Creation Date: (.+)\n", html)
    if(not match):
        match = re.search("Registration Date: (.+)\n", html)

    if(match):
        dt = match.group(1)

        datetime_object = datetime.strptime(dt.split("T")[0], "%Y-%m-%d")

        diff = (datetime.now() - datetime_object).days

        return diff
    return 0