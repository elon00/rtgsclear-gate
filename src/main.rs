//! Bounded offline arithmetic check, NOT an RTGS system or FIPS validation.
const MAX_BALANCE: u64 = i64::MAX as u64;

fn transfer_pair(sender: u64, receiver: u64, amount: u64) -> Result<(u64, u64), &'static str> {
    if amount == 0 || sender > MAX_BALANCE || receiver > MAX_BALANCE {
        return Err("invalid amount or balance");
    }
    let after_sender = sender.checked_sub(amount).ok_or("insufficient funds")?;
    let after_receiver = receiver.checked_add(amount).ok_or("overflow")?;
    if after_receiver > MAX_BALANCE {
        return Err("overflow");
    }
    Ok((after_sender, after_receiver))
}

fn main() {
    match transfer_pair(10, 4, 3) {
        Ok((sender, receiver)) if sender + receiver == 14 => {
            println!("Offline integer-balance invariant: PASS (no network or settlement)")
        }
        _ => std::process::exit(1),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn valid_pair_preserves_total() {
        assert_eq!(transfer_pair(10, 4, 3), Ok((7, 7)));
    }
    #[test]
    fn rejects_insufficient_funds() {
        assert!(transfer_pair(2, 0, 3).is_err());
    }
    #[test]
    fn rejects_overflow() {
        assert!(transfer_pair(10, MAX_BALANCE, 1).is_err());
    }
    #[test]
    fn rejects_zero_amount() {
        assert!(transfer_pair(10, 0, 0).is_err());
    }
}
