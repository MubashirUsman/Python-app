from fastapi import FastAPI, HTTPException, Query
import time
import dns.resolver

app = FastAPI()

@app.get("/dns-lookup")
def perform_dns_lookup(domain: str = Query(..., min_length=1), server: str = Query(..., min_length=1)):
    response_time = dns_lookup(domain, server)
    return {"domain": domain, "server": server, "response_time": response_time}


def dns_lookup(domain, server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server]

    start_time = time.time()
    try:
        answers = resolver.query(domain)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time
    except dns.exception.DNSException as e:
        print(f"Error querying {server}: {e}")
        raise HTTPException(status_code=500, detail=f"Error querying {server}: {e}")