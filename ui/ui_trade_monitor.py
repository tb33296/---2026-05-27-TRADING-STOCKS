# ui/ui_trade_monitor.py

# core/debug/trade_monitor_store.py

from collections import deque

class TradeMonitorStore:

    def __init__(self):

        self.events = deque(maxlen=500)

    def add(self, category, message):

        self.events.appendleft({
            "category": category,
            "message": message
        })

    def get_events(self):

        return list(self.events)


trade_monitor_store = TradeMonitorStore()