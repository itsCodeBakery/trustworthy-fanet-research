# FAN-GHETS24 v2 preflight result and low-bandwidth ZIP directory inspection

**Date:** 18 October 2026.

## Observed in researcher-operated Colab (uploaded report)

- Zenodo API reachable, record 13692267; **72 listed files and 18,648,943,241 declared bytes** match the expected split archive inventory.
- **87.16 GiB free** in transient Colab runtime. Split parts plus reconstructed ZIP would require approximately **34.74 GiB**, *before* extracted data and caches. Capacity for full extraction **not confirmed**.
- Published Zenodo [v2 record page](https://zenodo.org/records/13692267) identifies this exact record as **v2**; JSON `metadata.version` was absent (`null`). The old preflight wrongly classified absent *optional* version as a material `MISMATCH`. This check is corrected in [preflight script](../scripts/fan_ghets24_preflight.py); explicit conflicting version remains an error.
- Southampton GitLab anonymous project-tree API returned **HTTP 401**; the [public project HTML page](https://git.soton.ac.uk/ch1u20/fan-ghets24) is visible in a browser. The API status alone does **not** prove the source project is private.
- **No dataset bytes downloaded or real Parquet/JSON samples inspected yet.**

Source report SHA-256: `6d7d5f24ff9937d57e71bcb42bd8341f0658273b71575d1ebe2413806e8fe8b1`; the audit snapshot is in [evidence](../evidence/fan_ghets24_preflight_colab_2026-10-18.json).

## Next low-cost stage: terminal multipart-ZIP *directory* only

Because the dataset is 71 numbered `fan-ghets24.z01`–`.z71` parts and a final **36,719,241-byte** `fan-ghets24.zip`, the terminal part usually contains the ZIP **central directory**. Python's standard `zipfile.ZipFile(...).infolist()` can list this metadata even though the content spans missing volumes. This behavior was successfully tested on a **synthetic split ZIP**, *not yet on FAN-GHETS24*.

Execute in **Google Colab CPU**:

```python
!wget -q -O /content/inspect_fan_ghets24_directory.py https://raw.githubusercontent.com/itsCodeBakery/trustworthy-fanet-research/main/scripts/inspect_fan_ghets24_directory.py
!python /content/inspect_fan_ghets24_directory.py
```

The script uses the official Zenodo API to discover the terminal part, downloads **only that 36.7 MB file**, rejects unexpected size/MD5, and attempts **metadata-only** listing of archived paths and **total uncompressed bytes**. It counts Parquet/JSON entries and paired stems, and saves `/content/fan_ghets24_zip_directory.json`. It **does not extract, read a Parquet sample, or download the 71 other parts**.

If ZIP directory listing is unavailable without the earlier volumes, the script records a clear failure without treating that as dataset corruption. If successful, we can budget extraction and find meaningful sample paths *before* deciding whether to acquire the 18.65 GB release.

**Research boundary:** A directory entry filename or sequence count does not establish packet-level observability, attack timing, or independent physical simulation-family IDs. Actual Parquet/JSON inspection and new ns-3 traces remain prerequisites.

## Rationale

Using a temporary Colab runtime for an 18.65 GB multipart archive before knowing its uncompressed size and expected retained files is risky. The low-bandwidth ZIP directory audit is a genuinely useful stage in the project's reproducibility process, not a detour into unrelated model tuning.
