from fastapi import Request

def get_client_id(request: Request) -> str:
    return request.client.host   # IP-based for now