from flask import *
from playhouse.shortcuts import model_to_dict
import hashlib
import os
import re
import json
from datetime import datetime


app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

#################################################

# Rotas GET

@app.route('/stream')
def get_video2():
    path = "Episodio 1x7.mp4" # nome do arquivo
    start = 0
    end = None
    file_size = os.stat(path).st_size
    range_header = request.headers.get('Range', None)

    if range_header:
        byte1, byte2 = 0, None
        match = re.search(r'(\d+)-(\d*)', range_header)
        if match:
            g = match.groups()
            byte1 = int(g[0])
            if g[1]:
                byte2 = int(g[1])
            else:
                byte2 = file_size - 1
        start, end = byte1, byte2
    length = end - start + 1 if end is not None else file_size - start
    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
    
    response = Response(data, 206, mimetype="video/mp4", content_type="video/mp4", direct_passthrough=True)
    response.headers.add('Content-Range', f'bytes {start}-{start + length - 1}/{file_size}')
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Length', str(length))

    return response



@app.route('/')
def index():

    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
