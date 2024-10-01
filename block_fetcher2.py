from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from dotenv import load_dotenv
import os
import json
from decimal import Decimal

load_dotenv()

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def fetch_block_data(block_height):
    rpc_user = os.getenv("rpcUser")
    rpc_password = os.getenv("rpcPassword")
    rpc_host = os.getenv("rpcAddress")
    rpc_port = os.getenv("rpcPort")
    rpc_connection = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

    try:
        rpc_client = AuthServiceProxy(rpc_connection, timeout=120)
        block_hash = rpc_client.getblockhash(block_height)
        block_data = rpc_client.getblock(block_hash)
        return json.loads(json.dumps(block_data, cls=DecimalEncoder))
    except JSONRPCException as json_exception:
        print(f"A JSON RPC Exception occurred: {json_exception}")
    except Exception as general_exception:
        print(f"An error occurred: {general_exception}")
    return None