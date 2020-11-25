#!/bin/python

import hashlib
import json
import os

from bottle import route, run, static_file, response
import requests


CacheDir = None


def get_cache_file_path(url):
    filename = hashlib.sha512(url.encode('UTF-8')).hexdigest()
    return os.path.join(CacheDir, filename), os.path.join(CacheDir, filename + '.meta')

@route('/jump/<url:path>')
def jump(url):
    html = '''
<html>
    <head>
    <title>location.href</title>
    </head>
    <body>
        <input id="url" type="hidden" value="{}" />
        <script language="JavaScript">
            location.href = document.getElementById('url').getAttribute('value');
        </script>
    </body>
</html>
    '''.format(url)
    return html

@route('/proxy/<url:path>')
def proxy(url):
    content_path, meta_path = get_cache_file_path(url)

    if os.path.exists(content_path) and os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(fp=f)
        content_type = meta.get('Content-Type')
    else:
        res = requests.get(url)
        headers = res.headers
        content_type = headers.get('Content-Type')
        with open(content_path, 'bw') as f:
            f.write(res.content)
        with open(meta_path, 'w') as f:
            json.dump({'Content-Type': content_type}, fp=f)

    if content_type is not None:
        response.content_type = content_type

    with open(content_path, 'rb') as f:
        return f.read()

def main(cache='/tmp/nyamp', debug=False, port=8080, reloader=False):
    global CacheDir
    CacheDir = cache
    if not os.path.exists(CacheDir):
        os.makedirs(CacheDir)
    run(host='0.0.0.0', port=8080, debug=debug, reloader=reloader)

if __name__ == '__main__':
    import fire
    fire.Fire(main)
