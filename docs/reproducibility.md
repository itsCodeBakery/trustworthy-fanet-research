# Reproducibility and provenance

This is the repository's recording standard. Specific implementations and commands will be filled in only after execution and verification.

## Required information per run

1. **Identity:** experiment ID, date/time, source commit SHA, and script/notebook revision.
2. **Inputs:** dataset name, source/version, SHA-256 checksums, preprocessing, and split IDs.
3. **Configuration:** complete hyperparameters, evaluation settings, seeds, and simulation scenario.
4. **Environment:** Python/dependency versions, CUDA/driver/GPU if used, OS, SUMO and ns-3 version/build details where relevant.
5. **Execution:** exact command or Kaggle notebook commit/version, run status, duration, warnings, and any failures.
6. **Outputs:** prediction files or summaries, definition of every metric, aggregation rules, and hashes/locations of bulky artifacts.
7. **Statistical evidence:** number of independent runs, uncertainty intervals, significance tests (when applicable), and sampling units.

## Integrity rules

- Keep train/validation/test partitions independent and document any grouping that prevents leakage.
- Preserve raw measured outputs; derived tables and plots must be generated from traceable files.
- Separate completed, failed, and pending experiments; do not claim planned analyses were executed.
- Archive external data and artifacts at stable locations with checksums and access instructions.
- Record sources of non-determinism and limitations of the reproducibility environment.

This document specifies reporting requirements; it does not assert that the full pipeline has been run.
