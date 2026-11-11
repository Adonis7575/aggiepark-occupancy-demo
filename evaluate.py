"""Compare occupancy decision policies using synthetic scores."""
import csv
from pathlib import Path

from decisions import occupancy_label


LABELS = ("empty", "occupied")
DECISIONS = (*LABELS, "unknown")
SAMPLE = Path(__file__).with_name("sample_scores.csv")


def evaluate(examples, band):
    matrix = {label: dict.fromkeys(DECISIONS, 0) for label in LABELS}
    for label, score in examples:
        matrix[label][occupancy_label(score, band)] += 1

    total = sum(sum(row.values()) for row in matrix.values())
    accepted = total - sum(matrix[label]["unknown"] for label in LABELS)
    correct = sum(matrix[label][label] for label in LABELS)
    occupied = sum(matrix["occupied"].values())
    return {
        "coverage": accepted / total if total else None,
        "accepted_accuracy": correct / accepted if accepted else None,
        "false_opening_rate": matrix["occupied"]["empty"] / occupied if occupied else None,
        "matrix": matrix,
    }


def percent(value):
    return f"{value:.1%}" if value is not None else "n/a"


def main():
    with SAMPLE.open(encoding="utf-8", newline="") as file:
        examples = [(row["label"], float(row["score"])) for row in csv.DictReader(file)]

    for band in (0, 0.15):
        result = evaluate(examples, band)
        print(f"Uncertainty band {band:.2f}")
        for metric in ("coverage", "accepted_accuracy", "false_opening_rate"):
            print(f"  {metric.replace('_', ' ').capitalize():<20} {percent(result[metric])}")
        print("  Actual      Empty  Occupied  Unknown")
        for label, counts in result["matrix"].items():
            print(f"  {label:<10} {counts['empty']:>6} {counts['occupied']:>9} {counts['unknown']:>8}")
        print()


if __name__ == "__main__":
    main()
