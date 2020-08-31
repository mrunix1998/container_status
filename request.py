import subprocess
import shlex
from subprocess import check_output
import os
import simplejson as myjson

def send_request_to_api(container_name):
    data = '"{\\"EVENT_NAME\\": \\"UPDATE_SERVICES\\", \\"EVENT_BODY\\":{\\"CONTAINER_NAME\\": \\"postgres\\"}}"'
    print(data)
    data_json = myjson.dumps(data, default=myjson._default_decoder)
    cmd = 'curl --location -w %{http_code} --request POST "http://192.168.7.203:5002/routaa/api/secure/ui/log/public/save-data" ' \
              '--header "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwOTEyNDg1NTA0MyIsImlhdCI6MTU4ODEwMjMyMiwiZXhwIjoxNjE5NjM4MzIyfQ.ePrAixMU9Fu4HoNr3TCoiJMKMpRpLFkYvLCpa3Pnt1dn9ZenKaSKGokOv-GB9n9-yujHQ-M_RAEgtDBJ0v5V3w" --header "Content-Type: application/json" -d '+ data_json +' '''
    
    # cmd = 'curl --location -w %{http_code} --request POST "http://192.168.77.82:5002/routaa/api/secure/ui/log/public/save-data" ' \
    #       '--header "os: infra" --header "Authorization: Bearer ' \
    #       'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwOTEyNDg1NTA0MyIsImlhdCI6MTU4ODEwMjMyMiwiZXhwIjoxNjE5NjM4MzIyfQ' \
    #       '.ePrAixMU9Fu4HoNr3TCoiJMKMpRpLFkYvLCpa3Pnt1dn9ZenKaSKGokOv-GB9n9-yujHQ-M_RAEgtDBJ0v5V3w" --header ' \
    #       '"Content-Type: application/json" -d "{\"EVENT_NAME\":\"UPDATE_SERVICES\",\"EVENT_BODY\":{\"CONTAINER_NAME\":\"' + container_name + '"}}"'''

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
