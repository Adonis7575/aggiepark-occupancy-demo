# AggiePark occupancy evaluation

This portfolio demo evaluates a parking-space decision rule. A score near the boundary can produce **unknown**, so the application can avoid suggesting a space as open when the model is uncertain.

The example scores and labels are synthetic. This demo evaluates decisions from scores and does not train a model. It includes no camera imagery, campus records, or course submissions.

## Run

Use Python 3.10 or newer. The example requires no external packages.

```sh
python evaluate.py
python -m unittest
```

The command compares a binary rule with a 0.15 uncertainty band. It prints three metrics and a confusion matrix for each rule.

- **Coverage** is the fraction of all examples with an empty or occupied decision.
- **Accepted accuracy** is the fraction of those decisions that match the label.
- **False opening rate** is the fraction of truly occupied spaces labeled empty. Unknown spaces are excluded from the available count.

On the synthetic fixture, adding the band lowers the false opening rate from 50% to 25% and coverage from 100% to 75%. The underlying scores stay fixed. These figures explain the tradeoff in the example and do not estimate field performance.

The original AggiePark work explored this tradeoff on historical validation scores. This self-contained edition focuses on the decision rule and its evaluation.
