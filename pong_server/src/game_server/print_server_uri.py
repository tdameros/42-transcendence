import os
import subprocess
import sys


def get_server_uri():
    command = (f'lsof -a -p {os.getpid()} -i6'
               f" | awk '{{print $9}}'"
               f' | tail -n +2')
    """ gets all open ipv6 sockets for current process
                | gets the column with the uri of the socket
                | removes the first line which only contains the name
                  of the column """

    port: str = subprocess.check_output(command, shell=True).decode()
    if len(port) == 0:
        raise Exception('No open ipv6 sockets found')
    return f'http://{port if port[-1] != '\n' else port[:-1]}'


async def print_server_uri(sio):
    await sio.sleep(0.1)
    """ The async sleep is here so that the server starts before
        this function is executed """

    print(f'uri: {get_server_uri()}')
    """ Do not use logging()! This should always be printed as the redirection
        server will read it """
    sys.stdout.flush()
