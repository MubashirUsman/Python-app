from fastapi import FastAPI, HTTPException, Query
import time
from dns import resolver

app = FastAPI()

@app.get("/dns-lookup")
def perform_dns_lookup(domain: str = Query(..., min_length=1), server: str = Query(..., min_length=1)):
    response_time = dns_lookup(domain, server)
    return {"domain": domain, "server": server, "response_time": 1000*response_time}


def dns_lookup(domain, server):
    resolver_instance = resolver.Resolver()
    resolver_instance.nameservers = [server]

    start_time = time.time()
    try:
        answers = resolver.query(domain)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time
    except dns.exception.DNSException as e:
        print(f"Error querying {server}: {e}")
        raise HTTPException(status_code=500, detail=f"Error querying {server}: {e}")