from fastapi import FastAPI, Request
from redis.asyncio import Redis
import os


REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
REDIS_TTL: int = int(os.getenv("REDIS_TTL", 3600))

app = FastAPI()
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_client_ip(request: Request) -> str:
    x_forwarded_for: str | None = request.headers.get("X-Forwarded-For")
    
    if x_forwarded_for:
        return  x_forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host
            
    return "Unknown"


async def write_to_redis(client_hostname: str, client_ip: str):
    await redis.set(name=client_hostname, value=client_ip, ex=REDIS_TTL)


@app.get("/")
async def root(request: Request, client_hostname: str | None = None) -> dict[str, str]:
    client_ip: str = get_client_ip(request=request)

    if client_hostname:
        await write_to_redis(client_hostname, client_ip)

    return {"client_ip": client_ip}