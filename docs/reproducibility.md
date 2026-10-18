# Reproducibility requirements — UAV/FANET

**Status:** requirements, not execution evidence.

For every run record: experiment ID, **independent mission-family ID**, clean/attack/policy variant, code revision, exact simulator and software versions/build flags, exogenous mobility and offered-traffic hashes, radio/routing config, random stream assignments, observation-feature schema, relevant dataset checksums, train/dev/cal/test partition, decision deadline, frozen calibration artifact, and output/trace hashes.

Keep three separate classes of records: locally observable packet/radio events, *privileged evaluator-only* drop reason/attacker truth, and independent mission manifests. The deployable feature pipeline may never open privileged truth. Test that deleting its evaluator truth input cannot alter detector predictions.

Report all 2,743 runs as *planned* until verified executed. Never infer independent sample count from packet windows, monitoring views or repeated neural seeds. Bootstrap and compare at the mission-family level with paired variants retained. Every paper figure/table must be generated from actual saved run-level outcomes.

An all-benign complete-mission alarm calibration statement applies to the fixed 600 s horizon and **exchangeable** calibration/test missions with frozen detector. It does not establish false-accusation control under arbitrary mission/channel distribution shift. All violations, outages, false avoidance, and negative results must be reported.

The uploaded Overleaf package ZIP used for this scope alignment passed its local ZIP CRC check and has SHA-256 `6640605e9eb3bd3066b6bfc8e08a40bfa268c0f86e5c4d641b836545eb52891a`. This is provenance of the planning archive, **not** verification of an ns-3 run.
