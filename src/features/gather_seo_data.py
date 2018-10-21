from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import http.client, urllib.parse, uuid, json

def extract_metadata(url):
    #print("normal:" + url)
    abstr = ""
    desc = ""
    keywords = ""
    crashed = False
    try:
        try:
            content = urlopen(Request("https://" + url, headers={'User-Agent': 'Mozilla'}), timeout = 10)
        except:
            try:
                content = urlopen(Request("http://" + url, headers={'User-Agent': 'Mozilla'}), timeout = 10)
            except:
                raise
        soup = BeautifulSoup(content, 'html.parser')
        abstr = ""
        desc = ""
        keywords = ""
        for meta in soup.findAll("meta"):
            if not meta.has_attr('content'):
                continue
            metaname = meta.get('name', '').lower()
            metaprop = meta.get('property', '').lower()
            if 'description' == metaname or metaprop.find("description")>0:
                desc = meta['content'].strip()
            if 'abstract' == metaname or metaprop.find("abstract")>0:
                abstr = meta['content'].strip()
            if 'keywords' == metaname or metaprop.find("keywords")>0:
                keywords = meta['content'].strip()
    except Exception as e: 
            print(e)
            print(url)
            crashed = True
    return list(map(translate, keywords.split(',')))


def translate(text):
    if len(text) == 0:
        return

    # Replace the subscriptionKey string value with your valid subscription key.
    subscriptionKey = 'b1a0198a38694e8f91d7af82a2710ae3'

    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'

    # Translate to German and Italian.
    params = "&to=en";

    def __translate(content):
        headers = {
            'Ocp-Apim-Subscription-Key': subscriptionKey,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        conn = http.client.HTTPSConnection(host)
        conn.request("POST", path + params, content, headers)
        response = conn.getresponse()
        return response.read()

    requestBody = [{
        'Text': text,
    }]
    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
    result = __translate(content)

    # Note: We convert result, which is JSON, to and from an object so we can pretty-print it.
    # We want to avoid escaping any Unicode characters that result contains. See:
    # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
    output = json.loads(result)

    return output[0]['translations'][0]['text']
