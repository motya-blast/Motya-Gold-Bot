import json
import asyncio

trace_cfg = "C:\motya-gold\Telagram SO2 bot\src\cfg.json"
def get_kurs():
    with open(trace_cfg, "r")as file:
        kurs = json.load(file)
    return kurs["kurs"]

def get_sleep():
    with open(trace_cfg, "r")as file:
        sleep = json.load(file)
    return sleep["sleep"]