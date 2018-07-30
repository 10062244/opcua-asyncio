import os
# os.environ['PYOPCUA_NO_TYPO_CHECK'] = 'True'

import asyncio
import logging

from opcua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('opcua')


class SubscriptionHandler:
    def datachange_notification(self, node: Node, val, data):
        """Callback for opcua Subscription"""
        _logger.info('datachange_notification %r %s', node, val)


async def task(loop):
    url = 'opc.tcp://192.168.2.213:4840'
    # url = 'opc.tcp://localhost:4840/freeopcua/server/'
    client = Client(url=url)
    client.set_user('test')
    client.set_password('test')
    # client.set_security_string()
    await client.connect()
    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    root = client.get_root_node()
    _logger.info('Objects node is: %r', root)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    _logger.info('Children of root are: %r', await root.get_children())
    handler = SubscriptionHandler()
    subscription = await client.create_subscription(500, handler)
    nodes = [
        client.get_node('ns=1;i=6')
    ]
    await subscription.subscribe_data_change(nodes)


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.create_task(task(loop))
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
