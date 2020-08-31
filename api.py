# Attention: Dirty Code!
import subprocess
import time
import shlex
from subprocess import check_output
import os
import simplejson as myjson



# parse container info
def parse_line(line):
    result = []
    _str = ''
    for i in line:
        if i != b' '.decode('utf-8'):
            _str += i
        else:
            if _str:
                result.append(_str)
            _str = ''
    if _str:
        result.append(_str)
    return result


def get_active_containers():
    out = subprocess.Popen(["docker", "ps", "-a", "-f", "status=running"], stdout=subprocess.PIPE)
    out.stdout.readline()
    lines = str(out.stdout.read(), 'utf-8').split('\n')
    containers = []
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            containers.append({
                'name': parsed[-1],
                'id': parsed[0],
            })
    return containers


def container_is_active(active_containers, container_name):
    for i in active_containers:
        if i['name'] == container_name:
            return True
    return False


def send_request_to_api(container_name):
    data = '"{\\"EVENT_NAME\\": \\"UPDATE_SERVICES\\", \\"EVENT_BODY\\":{\\"CONTAINER_NAME\\": \\" ' + container_name + '\\"}}"'
    print(data)
    data_json = myjson.dumps(data, default=myjson._default_decoder)
    cmd = 'curl --location -w %{http_code} --request POST "http://192.168.7.203:5002/routaa/api/secure/ui/log/public/save-data" ' \
          '--header "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwOTEyNDg1NTA0MyIsImlhdCI6MTU4ODEwMjMyMiwiZXhwIjoxNjE5NjM4MzIyfQ.ePrAixMU9Fu4HoNr3TCoiJMKMpRpLFkYvLCpa3Pnt1dn9ZenKaSKGokOv-GB9n9-yujHQ-M_RAEgtDBJ0v5V3w" --header "Content-Type: application/json" -d ' + data_json + ' '''

    # print(cmd)
    subprocess.call(cmd, shell=True)
    devnull = open(os.devnull, 'wb', 0)
    http_code = int(check_output(shlex.split(cmd), stderr=devnull))

    if http_code == 204:
        print("\n --- Send Request is Successful ---")
    else:
        print("\n --- Send Request is Failed ---")


def watch_containers(container_names_list, check_interval_seconds=15):
    while True:
        active_containers = get_active_containers()
        print(active_containers)
        for c in container_names_list:
            if container_is_active(active_containers, c):
                print(c, " IS ACTIVE ")
            else:
                print(f"{c} IS NOT ACTIVE :: SAVE DATE TO RESTART OR DEBUG")
                # date = datetime.datetime.now()
                # today = str(date.today())
                send_request_to_api(c)
        print("----------------------------")
        time.sleep(check_interval_seconds)


if __name__ == '__main__':
    watch_containers(['yourls', 'postgres', 'mysql'], check_interval_seconds=4)
