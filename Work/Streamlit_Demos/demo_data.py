from pathlib import Path
import csv


DATA_DIR = Path(__file__).resolve().parents[1] / "Data"


def read_portfolio(filename=DATA_DIR / "portfolio.csv"):
    portfolio = []
    with open(filename, newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if not row or not row.get("name"):
                continue
            portfolio.append(
                {
                    "name": row["name"],
                    "shares": int(row["shares"]),
                    "price": float(row["price"]),
                }
            )
    return portfolio


def read_prices(filename=DATA_DIR / "prices.csv"):
    prices = {}
    with open(filename, newline="") as file:
        rows = csv.reader(file)
        for row in rows:
            if not row or not any(item.strip() for item in row):
                continue
            name, price = row
            prices[name] = float(price)
    return prices


def make_report(portfolio, prices):
    report = []
    for holding in portfolio:
        current_price = prices.get(holding["name"])
        if current_price is None:
            continue

        cost = holding["shares"] * holding["price"]
        value = holding["shares"] * current_price
        report.append(
            {
                "name": holding["name"],
                "shares": holding["shares"],
                "purchase_price": holding["price"],
                "current_price": current_price,
                "cost": cost,
                "value": value,
                "change": value - cost,
                "return_pct": (value - cost) / cost,
            }
        )
    return report


def load_report():
    return make_report(read_portfolio(), read_prices())


def filter_report(report, selected_names, minimum_value=0, losers_only=False):
    return [
        row
        for row in report
        if row["name"] in selected_names
        and row["value"] >= minimum_value
        and (not losers_only or row["change"] < 0)
    ]


def summarize(report):
    total_cost = sum(row["cost"] for row in report)
    total_value = sum(row["value"] for row in report)
    gain_loss = total_value - total_cost
    return total_cost, total_value, gain_loss


def holdings_by_name(report):
    totals = {}
    for row in report:
        name = row["name"]
        totals.setdefault(name, {"name": name, "value": 0.0, "cost": 0.0, "change": 0.0})
        totals[name]["value"] += row["value"]
        totals[name]["cost"] += row["cost"]
        totals[name]["change"] += row["change"]
    return list(totals.values())

