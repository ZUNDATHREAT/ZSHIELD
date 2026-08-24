#!/usr/bin/env python3
"""ZSHIELD local dashboard server — standard-library only."""
from __future__ import annotations
import base64, json, os, shutil, socket, time, urllib.error, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STATIC=ROOT/"static"
PORT=int(os.getenv("ZSHIELD_PORT","8080"))
ADGUARD_URL=os.getenv("ADGUARD_URL","http://127.0.0.1").rstrip("/")
ADGUARD_USERNAME=os.getenv("ADGUARD_USERNAME","")
ADGUARD_PASSWORD=os.getenv("ADGUARD_PASSWORD","")

def read(path,default=""):
    try:return Path(path).read_text().strip()
    except OSError:return default

def memory():
    values={}
    for line in read("/proc/meminfo").splitlines():
        key,_,value=line.partition(":")
        try:values[key]=int(value.strip().split()[0])*1024
        except (ValueError,IndexError):pass
    total=values.get("MemTotal",0)
    return {"total":total,"used":max(0,total-values.get("MemAvailable",0))}

def temperature():
    try:return round(float(read("/sys/class/thermal/thermal_zone0/temp"))/1000,1)
    except ValueError:return None

def local_ip():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1",80));return sock.getsockname()[0]
    except OSError:return "127.0.0.1"
    finally:sock.close()

def adguard(path):
    request=urllib.request.Request(f"{ADGUARD_URL}{path}")
    if ADGUARD_USERNAME:
        token=base64.b64encode(f"{ADGUARD_USERNAME}:{ADGUARD_PASSWORD}".encode()).decode()
        request.add_header("Authorization",f"Basic {token}")
    with urllib.request.urlopen(request,timeout=2.5) as response:return json.load(response)

def status():
    disk=shutil.disk_usage("/")
    payload={"generated_at":int(time.time()),"node":{"hostname":socket.gethostname(),"ip":local_ip(),"system_uptime_seconds":float(read("/proc/uptime","0").split()[0]),"temperature_c":temperature(),"memory":memory(),"disk":{"total":disk.total,"used":disk.used}},"adguard":{"online":False,"dns_queries":0,"blocked_filtering":0,"replaced_safebrowsing":0,"replaced_parental":0,"avg_processing_time":0}}
    try:
        stats=adguard("/control/stats")
        payload["adguard"].update({"online":True,"dns_queries":stats.get("num_dns_queries",0),"blocked_filtering":stats.get("num_blocked_filtering",0),"replaced_safebrowsing":stats.get("num_replaced_safebrowsing",0),"replaced_parental":stats.get("num_replaced_parental",0),"avg_processing_time":stats.get("avg_processing_time",0)})
    except (OSError,ValueError,urllib.error.URLError,json.JSONDecodeError):pass
    return payload

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(STATIC),**kwargs)
    def do_GET(self):
        if self.path.split("?",1)[0]=="/api/status":
            body=json.dumps(status()).encode();self.send_response(200);self.send_header("Content-Type","application/json");self.send_header("Cache-Control","no-store");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
        if self.path=="/health":
            body=b'{"ok":true}';self.send_response(200);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
        if self.path=="/":self.path="/index.html"
        super().do_GET()
    def end_headers(self):
        self.send_header("Content-Security-Policy","default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'");self.send_header("Referrer-Policy","no-referrer");self.send_header("X-Content-Type-Options","nosniff");super().end_headers()

if __name__=="__main__":
    server=ThreadingHTTPServer(("0.0.0.0",PORT),Handler);print(f"ZSHIELD dashboard: http://0.0.0.0:{PORT}")
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
