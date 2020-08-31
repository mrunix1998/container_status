import subprocess
import shlex
from subprocess import check_output
import os
import simplejson as myjson

def send_request_to_api(container_name):
    data = '"{\\"EVENT_NAME\\": \\"UPDATE_SERVICES\\", \\"EVENT_BODY\\":{\\"CONTAINER_NAME\\": \\"postgres\\"}}"'
    print(data)
    data_json = myjson.dumps(data, default=myjson._default_decoder)
    cmd = 'curl --location -w %{http_code} --request POST "http://your-api" ' \
              '--header "Authorization: your-api-token " --header "Content-Type: application/json" -d '+ data_json +' '''

    # print(cmd)
    subprocess.call(cmd, shell=True)
    # DEVNULL = open(os.devnull, 'wb', 0)
    # http_code = int(check_output(shlex.split(cmd), stderr=DEVNULL))
    #
    # if http_code == 204:
    #     print(" ok")
    # else:
    #     print("\nnok")


send_request_to_api('yourls')
