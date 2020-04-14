import asyncio
from typing import List, Tuple
import logging
import time

logging.getLogger().setLevel(logging.INFO)

DEFAULT_TIMEOUT = 3  # seconds


def execute_socket_checks(addresses: List[Tuple[str, int]], timeout=None) -> dict:
    timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
    start = time.time()
    loop = asyncio.new_event_loop()
    tasks = [loop.create_task(check_socket_is_open(host, port, timeout=timeout)) for host, port in addresses]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    end = time.time()

    # Prepare output
    no_of_addresses = len(addresses)
    no_of_open_sockets = len([i for i in results if i['connection_succeeded']])
    res = {
        'results': results,
        'total_duration_seconds': end-start,
        'open': no_of_open_sockets,
        'closed': no_of_addresses - no_of_open_sockets,
        'total': no_of_addresses,
        'timeout_seconds': timeout
    }
    return res


async def check_socket_is_open(host: str, port: int, timeout=DEFAULT_TIMEOUT) -> dict:
    connection_succeeded = False
    try:
        await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        connection_succeeded = True
    except asyncio.exceptions.TimeoutError:
        logging.info(f'Check for {host}:{port} timed out ({timeout}s)')
    except Exception as ex:
        logging.info(f'Check for {host}:{port} {ex}')
    return {'host': host, 'port': port, 'connection_succeeded': connection_succeeded}
