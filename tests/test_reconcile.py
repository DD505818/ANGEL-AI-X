from backend.oms.reconcile import OMSReconciler


class DummyOrder:
    def __init__(self):
        self.venue = "binance"
        self.client_key = "ANGEL:test"
        self.order_id = 1
        self.px = 100.0
        self.qty = 1.0
        self.tick_size = 0.01
        self.status = "NEW"


class DummyLedger:
    def list_open_orders(self):
        return [DummyOrder()]

    def mark_cancelled(self, oid, reason):
        self.cancelled = (oid, reason)

    def mark_ack(self, oid, vid):
        self.acked = (oid, vid)


class DummyVenue:
    def __init__(self, name):
        self.name = name

    def list_open_orders(self):
        return []


class DummyOMS:
    def replace(self, *a, **k):
        self.replaced = (a, k)


def test_reconcile_cancels_missing():
    rec = OMSReconciler([DummyVenue("binance")], DummyLedger(), DummyOMS())
    res = rec.reconcile_all()
    assert res["cancelled_stale"] == 1
