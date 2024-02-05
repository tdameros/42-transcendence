import subprocess


async def get_server_uri(sio, pid):
    await sio.sleep(0.1)
    """ The async sleep is here so that the server starts before
        this function is executed """

    command = (f'lsof -a -p {pid} -i4'
               f" | awk '{{print $9}}'"
               f' | tail -n +2')
    """ gets all open ipv4 sockets for current process
                | gets the column with the uri of the socket
                | removes the first line which only contains the name
                  of the column """

    port: str = subprocess.check_output(command, shell=True).decode()
    if len(port) == 0:
        raise Exception('No open ipv4 sockets found')
    return f'http://localhost{port if port[-1] != '\n' else port[1:-1]}'
    # TODO this only works on localhost
