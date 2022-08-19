import schedule as schedule
from flask import Flask, request
from info_util import get_info
from time import time
from gevent.pywsgi import WSGIServer
import argparse
import json

app = Flask(__name__)
server_key = 'server_key'  # This will be loaded, not real value


def update_info():
    global info
    info = get_info()
    info['last_update'] = time()


update_info()


@app.route('/')
def return_stats():
    given_key = request.args.get('key', default='', type=str)
    if given_key != server_key:
        return 'Invalid key', 403
    return info


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='Port to listen on')
    parser.add_argument('-c', '--code', type=str, help='Key to use to access the stats')
    parser.add_argument('-dc', '--default-code', type=str, help='Set a code as default')
    parser.add_argument('-dp', '--default-port', type=int, help='Set a port port as default')
    parser.add_argument('-dr', '--default-refresh', type=int, help='Set how often to update the stats (in seconds)')
    parser.add_argument('-d', '--debug', action='store_true', help='Run on Flask debug server')
    args = parser.parse_args()

    # Save items if requested
    if args.default_code or args.default_port or args.default_refresh:
        data = json.load(open('config.json'))

        if args.default_code:
            data['code'] = args.default_code
        if args.default_port:
            data['port'] = args.default_port
        if args.default_refresh:
            data['update_seconds'] = args.default_refresh
        with open('config.json', 'w') as f:
            json.dump(data, f)
        print('Changed following items:')
        if args.default_code:
            print(f'\tcode: {args.default_code}')
        if args.default_port:
            print(f'\tport: {args.default_port}')
        if args.default_refresh:
            print(f'\tupdate_seconds: {args.default_refresh}')
        exit()

    # Load in code
    if args.code:
        server_key = args.code
    else:
        with open('config.json', 'r') as f:
            server_key = json.load(f)['code']
    if args.port:
        server_port = args.port
    else:
        with open('config.json', 'r') as f:
            server_port = json.load(f)['port']

    # Schedule update
    # Stored in config.json
    schedule.every(json.load(open('config.json'))['update_seconds']).seconds.do(update_info)

    if args.debug:
        print('Running on Flask debug server')
        app.run(debug=True, port=server_port)
    else:
        http_server = WSGIServer(('', server_port), app)
        http_server.serve_forever()
