from pathlib import Path

from ingest.csv_import import load_bofa_csv
from ingest.txt_import import load_bofa_txt
from rules.transfers import filter_transfers
from reports.summary import total_balance


def main():
    transactions = []

    transactions += load_bofa_txt(
        Path("data/checking.txt"),
        account_name="checking",
    )

    # You can mix formats later if needed
    # transactions += load_bofa_csv(Path("data/savings.csv"), "savings")

    cleaned = filter_transfers(transactions)
    balance = total_balance(cleaned)

    print(f"Merged Balance: ${balance}")


if __name__ == "__main__":
    main()
