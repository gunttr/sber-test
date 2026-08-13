from fastapi import FastAPI, Request

app = FastAPI()


def get_client_ip(request: Request) -> str:
    x_forwarded_for: str | None = request.headers.get("X-Forwarded-For")
    
    if x_forwarded_for:
        return  x_forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host
            
    return "Unknown"


async def write_to_redis(client_hostname: str, client_ip: str):
    with open("redis.txt", "a") as file:
        file.write(f"{client_hostname}: {client_ip}\n")


@app.get("/")
async def root(request: Request, client_hostname: str | None = None) -> dict[str, str]:
    client_ip: str = get_client_ip(request=request)

    if client_hostname:
        await write_to_redis(client_hostname, client_ip)

    return {"client_ip": client_ip}