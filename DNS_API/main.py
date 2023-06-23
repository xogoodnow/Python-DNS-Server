from flask import Flask, request, make_response
import subprocess
from logging import info
from logging.config import dictConfig
import re

app = Flask(__name__)

@app.route('/dns', methods=["POST"])
def dns_api():
    data = request.json
    domain = data['domain']
    protocol = data['protocol']
    if protocol == 'tcp':
        protocol = '+tcp'
    elif protocol == 'udp':
        protocol = ''
    else:
        return make_response({'message': 'Unsupported protocol'}, 422)

    info('i reached here')
    query_response = subprocess.check_output(f'dig {domain} @127.0.0.1 -p 5000 {protocol}', shell=True)
    info(f'command response is {query_response}')
    query_response = query_response.decode('utf-8')
    query_response = query_response.replace('\n', '  ')
    query_response = query_response.replace('\t', '  ')
    query_response = '  '.join(query_response.split())

    # pattern = re.compile(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}')
    # ips = pattern.findall(query_response)
    # valid_ips= []
    # for i in ips:
    #     if i[0] != '127':
    #         valid_ips.append(''.join(i))
    #

    return make_response({"result": query_response}, 200)







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
