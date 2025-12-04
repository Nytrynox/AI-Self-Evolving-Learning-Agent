"""Simple Agent Event Bus
=======================
Append-only JSON log of agent events for cross-agent awareness.
"""
from pathlib import Path
import json, threading, time

_BUS_PATH = Path("aurora_memory/agent_events.json")
_lock = threading.Lock()

_DEF = {"version":1,"events":[]}
MAX_EVENTS = 500

def _load():
    if not _BUS_PATH.exists():
        return dict(_DEF)
    try:
        return json.loads(_BUS_PATH.read_text())
    except Exception:
        return dict(_DEF)

def _save(data):
    tmp=_BUS_PATH.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2), encoding='utf-8')
    tmp.replace(_BUS_PATH)

def publish(event_type:str, payload:dict):
    with _lock:
        data=_load()
        data['events'].append({
            'ts': time.time(),
            'type': event_type,
            'payload': payload
        })
        data['events']=data['events'][-MAX_EVENTS:]
        _save(data)

def recent(limit:int=50):
    data=_load()
    return data['events'][-limit:]

# Convenience accessor
class EventBus:
    def publish(self, event_type:str, payload:dict):
        publish(event_type, payload)
    def recent(self, limit:int=50):
        return recent(limit)

_bus = None

def get_event_bus():
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus
