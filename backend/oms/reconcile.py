"""Order Management System reconciliation utilities."""
from typing import List, Dict

class OMSReconciler:
    """
    On reconnect: pull open orders from venue(s), diff with ledger, fix drifts.
    States: NEW, ACK, PARTIAL, FILLED, CANCELLED, REJECT
    """
    def __init__(self, venues, ledger, oms):
        self.venues = venues
        self.ledger = ledger
        self.oms = oms

    def reconcile_all(self) -> Dict[str, int]:
        fixed = {"cancelled_stale":0, "replaced":0, "ack_synced":0}
        open_ledger = self.ledger.list_open_orders()     # local truth
        by_venue = {}
        for v in self.venues:
            by_venue[v.name] = v.list_open_orders()      # remote truth

        for lo in open_ledger:
            remote = by_venue.get(lo.venue, [])
            match = next((ro for ro in remote if ro.client_key == lo.client_key), None)
            if not match:
                # Ledger says open but venue doesn't know — cancel locally + mark cancelled
                self.ledger.mark_cancelled(lo.order_id, reason="VenueMissing")
                fixed["cancelled_stale"] += 1
                continue
            # Sync price/qty if drifted (venue replace emulation)
            if (abs(match.px - lo.px) > lo.tick_size) or (match.qty != lo.qty):
                self.oms.replace(lo, px=lo.px, qty=lo.qty)
                fixed["replaced"] += 1
            # Mark ack if venue has an order our ledger thinks is NEW
            if lo.status == "NEW" and match.status in ("ACK","PARTIAL"):
                self.ledger.mark_ack(lo.order_id, match.venue_order_id)
                fixed["ack_synced"] += 1
        return fixed

