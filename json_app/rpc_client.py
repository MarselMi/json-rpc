import json
import ssl
import urllib.request
from django.conf import settings

def call_jsonrpc_method(url, method, params=None):
    if params is None:
        params = {}
    headers = {'Content-Type': 'application/json'}
    payload = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': 1,
    }
    data = json.dumps(payload).encode('utf-8')
    
    cert_file = "/tmp/cert.pem"
    key_file = "/tmp/key.pem"

    # Записываем сертификаты во временные файлы
    with open(cert_file, "w") as cert:
        cert.write(settings.CERTIFICATE)

    with open(key_file, "w") as key:
        key.write(settings.PRIVATE_KEY)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data)
    except urllib.error.HTTPError as e:
        return {'error': str(e)}
    except urllib.error.URLError as e:
        return {'error': str(e)}