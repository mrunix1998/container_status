# Attention: Dirty Code!
import subprocess
import time
import psycopg2
import datetime


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


def send_request_to_database(container_name, restart_date):
    try:
        connection = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432", database="date")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO container_status(container_name, date)VALUES('{0}','{1}') ON CONFLICT (container_name) DO UPDATE SET "date"=excluded.date, "container_name"=excluded.container_name;""".format(container_name, restart_date)
        record_to_insert = (container_name, restart_date)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "* Record inserted successfully into date table")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("* Failed to insert record into date table", "-->", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("* PostgreSQL connection is closed")


def watch_containers(container_names_list, check_interval_seconds=10):
    while True:
        active_containers = get_active_containers()
        print(active_containers)
        for c in container_names_list:
            if container_is_active(active_containers, c):
                print(c, " IS ACTIVE ")
            else:
                print(f"{c} IS NOT ACTIVE :: SAVE DATE TO RESTART OR DEBUG")
                date = datetime.datetime.now()
                today = str(date.today())
                send_request_to_database(c, today)
        print("----------------------------")
        time.sleep(check_interval_seconds)


if __name__ == '__main__':
    watch_containers(['yourls', 'postgres', 'mysql'], check_interval_seconds=1)
