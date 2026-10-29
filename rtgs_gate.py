"""Bounded, offline RTGS accounting invariant checker (not a payment system).

All amounts are integer minor units. No network, credentials, ledger persistence,
finality, identity verification, or real settlement is implemented.
"""
from dataclasses import dataclass
from typing import Collection, Iterable, Mapping
import re

MAX_BALANCE = (1 << 63) - 1
_ID = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
_CURRENCY = re.compile(r"[A-Z]{3,12}\Z")


class SettlementError(ValueError):
    """A proposed offline batch violated an accounting invariant."""


@dataclass(frozen=True)
class Transfer:
    transfer_id: str
    sender: str
    receiver: str
    currency: str
    amount: int


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise SettlementError(f"INVALID_{name}")
    return value


def _currency(value: object) -> str:
    if not isinstance(value, str) or _CURRENCY.fullmatch(value) is None:
        raise SettlementError("INVALID_CURRENCY")
    return value


def _amount(value: object, *, allow_zero: bool) -> int:
    if type(value) is not int or value < (0 if allow_zero else 1) or value > MAX_BALANCE:
        raise SettlementError("INVALID_AMOUNT")
    return value


def apply_batch(
    balances: Mapping[tuple[str, str], int],
    transfers: Iterable[Transfer],
    seen_ids: Collection[str],
) -> tuple[dict[tuple[str, str], int], set[str]]:
    """Validate and return an all-or-nothing *copy* of an offline transfer batch.

    The caller must persist and serialize both returned values atomically to
    obtain durable replay protection. This function deliberately does neither.
    """
    if not isinstance(balances, Mapping):
        raise SettlementError("INVALID_BALANCES")
    working = {}
    for key, balance in balances.items():
        if not isinstance(key, tuple) or len(key) != 2:
            raise SettlementError("INVALID_ACCOUNT_KEY")
        _identifier(key[0], "ACCOUNT")
        _currency(key[1])
        working[key] = _amount(balance, allow_zero=True)
    if isinstance(seen_ids, (str, bytes)):
        raise SettlementError("INVALID_SEEN_IDS")
    try:
        new_seen = set(seen_ids)
    except (TypeError, ValueError) as exc:
        raise SettlementError("INVALID_SEEN_IDS") from exc
    for item in new_seen:
        _identifier(item, "TRANSFER_ID")
    if len(new_seen) != len(seen_ids):
        raise SettlementError("DUPLICATE_SEEN_IDS")
    try:
        batch = tuple(transfers)
    except TypeError as exc:
        raise SettlementError("INVALID_BATCH") from exc
    if not batch:
        raise SettlementError("EMPTY_BATCH")
    for transfer in batch:
        if not isinstance(transfer, Transfer):
            raise SettlementError("INVALID_TRANSFER")
        tid = _identifier(transfer.transfer_id, "TRANSFER_ID")
        sender = _identifier(transfer.sender, "ACCOUNT")
        receiver = _identifier(transfer.receiver, "ACCOUNT")
        currency = _currency(transfer.currency)
        amount = _amount(transfer.amount, allow_zero=False)
        if sender == receiver:
            raise SettlementError("SELF_TRANSFER")
        if tid in new_seen:
            raise SettlementError("DUPLICATE_OR_REPLAYED_TRANSFER")
        source, target = (sender, currency), (receiver, currency)
        before_source = working.get(source, 0)
        before_target = working.get(target, 0)
        if before_source < amount:
            raise SettlementError("INSUFFICIENT_FUNDS")
        if before_target > MAX_BALANCE - amount:
            raise SettlementError("BALANCE_OVERFLOW")
        working[source] = before_source - amount
        working[target] = before_target + amount
        new_seen.add(tid)
    return working, new_seen
