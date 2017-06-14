import urllib
import requests
import random
import http


def get_html_doc(url):
    UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
           "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
           )
    ua = UAS[random.randrange(len(UAS))]
    headers = {
        'User-Agent': ua
    }
    req = urllib.request.Request(
        url,
        data=None,
        headers=headers
    )
    try:
        html_doc = urllib.request.urlopen(url).read()
    except (urllib.error.HTTPError, http.client.RemoteDisconnected, requests.exceptions.ConnectionError) as e:
        try:
            response = requests.get(url, headers=headers)
            html_doc = response.content
        except (TypeError, urllib.error.HTTPError, http.client.RemoteDisconnected, requests.exceptions.ConnectionError):
            return None
    return html_doc

    def get_timestamp(self, site_name):
        if os.path.isfile("data/timestamps.json"):
            with open("data/timestamps.json", 'r') as f:
                timestamps = json.load(f)
                f.close()
                if timestamps[site_name]:
                    return timestamps[site_name]
                else: 
                    return 0

    def set_timestamp(self, site_name, timestamp):
        if os.path.isfile("data/timestamps.json"):
            with open("data/timestamps.json", 'r') as f:
                timestamps = json.load(f)
                timestamps[site_name] = timestamp
                f.close()

