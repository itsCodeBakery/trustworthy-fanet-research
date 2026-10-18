# Experiment registry

Each completed run should have a unique identifier linked to:

- Git commit SHA and execution command / Kaggle notebook version.
- Dataset manifest and fixed train/validation/test split identifiers.
- Configuration file, random seeds, software versions and hardware metadata.
- Outputs, validated metrics, warnings, failure status, and elapsed time.
- Linked simulation scenario and statistical-analysis configuration, where applicable.

Use separate IDs for pilot runs, ablations, final evaluations, and failed runs. Never overwrite a prior run's metadata to make results appear cleaner.

**Status:** No runs recorded yet.
