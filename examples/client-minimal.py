
import asyncio
import logging

from opcua import Client

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('opcua')


async def task(loop):
    url = "opc.tcp://commsvr.com:51234/UA/CAS_UA_Server"
    # url = "opc.tcp://localhost:4840/freeopcua/server/"
    try:
        async with Client(url=url) as client:
            # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
            root = client.get_root_node()
            _logger.info("Objects node is: %r", root)

            # Node objects have methods to read and write node attributes as well as browse or populate address space
            _logger.info("Children of root are: %r", await root.get_children())

            # get a specific node knowing its node id
            # var = client.get_node(ua.NodeId(1002, 2))
            # var = client.get_node("ns=3;i=2002")
            # print(var)
            # var.get_data_value() # get value of node as a DataValue object
            # var.get_value() # get value of node as a python builtin
            # var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
            # var.set_value(3.9) # set node value using implicit data type

            # Now getting a variable node using its browse path
            myvar = await root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
            obj = await root.get_child(["0:Objects", "2:MyObject"])
            _logger.info("myvar is: %r", myvar)
    except Exception:
        _logger.exception('error')


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(task(loop))
    loop.close()


if __name__ == "__main__":
    main()
