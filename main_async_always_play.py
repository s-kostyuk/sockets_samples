#!/usr/bin/env python

import asyncio

TCP_IP = '127.0.0.1'
TCP_PORT = 6600
BUFFER_SIZE = 1024

async def mpd_client(loop):
    reader, writer = await asyncio.open_connection(host=TCP_IP, port=TCP_PORT, loop=loop)

    data = await reader.read(BUFFER_SIZE)

    if data.startswith(b'OK'):
        print("Connection succeed: ", data, flush=True)

    idle_command_string = "idle\n"

    async def read_data():
        # Returns something like this: b'changed: player\nOK\n'
        data = await reader.read(BUFFER_SIZE)  # type: bytes

        nonlocal data_counter

        print(data_counter, "Received: ", data, flush=True)

        data_counter += 1

    def write_data(data: bytes):
        # All communication data is encoded in UTF-8
        writer.write(data)
        print("\nCommand send: {0}".format(data))

    data_counter = 0

    while True:
        write_data(idle_command_string.encode(encoding='utf-8'))

        asyncio.sleep(1)

        write_data("noidle\n".encode(encoding='utf-8'))

        await read_data()

        asyncio.sleep(1)

        write_data("play\n".encode(encoding='utf-8'))

        await read_data()

        asyncio.sleep(1)

        write_data(idle_command_string.encode(encoding='utf-8'))

        await read_data()

        asyncio.sleep(1)


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(mpd_client(loop))
except KeyboardInterrupt:
    pass
finally:
    loop.close()
