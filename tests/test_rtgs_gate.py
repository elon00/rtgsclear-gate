import unittest
from rtgs_gate import MAX_BALANCE, SettlementError, Transfer, apply_batch


def tx(tid="t1", sender="alice", receiver="bob", currency="USD", amount=3):
    return Transfer(tid, sender, receiver, currency, amount)


class OfflineSettlementTests(unittest.TestCase):
    def setUp(self):
        self.balances = {("alice", "USD"): 10, ("bob", "USD"): 4}
        self.seen = set()

    def test_valid_transfer(self):
        b, s = apply_batch(self.balances, [tx()], self.seen)
        self.assertEqual((b[("alice", "USD")], b[("bob", "USD")]), (7, 7))
        self.assertEqual(s, {"t1"})

    def test_inputs_not_mutated(self):
        apply_batch(self.balances, [tx()], self.seen)
        self.assertEqual(self.balances, {("alice", "USD"): 10, ("bob", "USD"): 4})
        self.assertEqual(self.seen, set())

    def test_batch_is_atomic_on_failure(self):
        original = self.balances.copy()
        with self.assertRaisesRegex(SettlementError, "INSUFFICIENT_FUNDS"):
            apply_batch(self.balances, [tx(), tx("t2", amount=100)], self.seen)
        self.assertEqual(self.balances, original)
        self.assertEqual(self.seen, set())

    def test_replay_rejected(self):
        with self.assertRaisesRegex(SettlementError, "DUPLICATE_OR_REPLAYED"):
            apply_batch(self.balances, [tx()], {"t1"})

    def test_duplicate_within_batch_rejected(self):
        with self.assertRaisesRegex(SettlementError, "DUPLICATE_OR_REPLAYED"):
            apply_batch(self.balances, [tx(), tx()], self.seen)

    def test_zero_amount_rejected(self):
        with self.assertRaisesRegex(SettlementError, "INVALID_AMOUNT"):
            apply_batch(self.balances, [tx(amount=0)], self.seen)

    def test_negative_amount_rejected(self):
        with self.assertRaises(SettlementError):
            apply_batch(self.balances, [tx(amount=-1)], self.seen)

    def test_bool_amount_rejected(self):
        with self.assertRaises(SettlementError):
            apply_batch(self.balances, [tx(amount=True)], self.seen)

    def test_float_amount_rejected(self):
        with self.assertRaises(SettlementError):
            apply_batch(self.balances, [tx(amount=1.5)], self.seen)

    def test_overflow_rejected(self):
        with self.assertRaisesRegex(SettlementError, "BALANCE_OVERFLOW"):
            apply_batch({("alice", "USD"): 10, ("bob", "USD"): MAX_BALANCE}, [tx()], self.seen)

    def test_invalid_existing_balance_rejected(self):
        with self.assertRaises(SettlementError):
            apply_batch({("alice", "USD"): -1}, [tx()], self.seen)

    def test_self_transfer_rejected(self):
        with self.assertRaisesRegex(SettlementError, "SELF_TRANSFER"):
            apply_batch(self.balances, [tx(receiver="alice")], self.seen)

    def test_invalid_currency_rejected(self):
        with self.assertRaisesRegex(SettlementError, "INVALID_CURRENCY"):
            apply_batch(self.balances, [tx(currency="usd")], self.seen)

    def test_invalid_identifier_rejected(self):
        with self.assertRaisesRegex(SettlementError, "INVALID_TRANSFER_ID"):
            apply_batch(self.balances, [tx(tid="../evil")], self.seen)

    def test_currency_isolation(self):
        with self.assertRaisesRegex(SettlementError, "INSUFFICIENT_FUNDS"):
            apply_batch(self.balances, [tx(currency="EUR", amount=1)], self.seen)

    def test_valid_two_step_batch(self):
        b, s = apply_batch(self.balances, [tx(), tx("t2", "bob", "carol", amount=2)], self.seen)
        self.assertEqual(b[("alice", "USD")], 7)
        self.assertEqual(b[("bob", "USD")], 5)
        self.assertEqual(b[("carol", "USD")], 2)
        self.assertEqual(s, {"t1", "t2"})

    def test_empty_batch_rejected(self):
        with self.assertRaisesRegex(SettlementError, "EMPTY_BATCH"):
            apply_batch(self.balances, [], self.seen)

    def test_bad_transfer_shape_rejected(self):
        with self.assertRaisesRegex(SettlementError, "INVALID_TRANSFER"):
            apply_batch(self.balances, [{"amount": 3}], self.seen)

    def test_invalid_account_key_rejected(self):
        with self.assertRaisesRegex(SettlementError, "INVALID_ACCOUNT_KEY"):
            apply_batch({"alice": 10}, [tx()], self.seen)

    def test_duplicate_seen_ids_rejected(self):
        with self.assertRaisesRegex(SettlementError, "DUPLICATE_SEEN_IDS"):
            apply_batch(self.balances, [tx()], ["prior", "prior"])

    def test_conservation_per_currency(self):
        b, _ = apply_batch(self.balances, [tx(), tx("t2", "bob", "carol", amount=2)], self.seen)
        self.assertEqual(sum(v for (a, c), v in self.balances.items() if c == "USD"),
                         sum(v for (a, c), v in b.items() if c == "USD"))


if __name__ == "__main__":
    unittest.main()
