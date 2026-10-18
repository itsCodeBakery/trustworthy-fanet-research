# FAN-GHETS24 v2 — Colab metadata and storage preflight

**Status:** ready to execute, **not executed on the public dataset in this commit**. No Parquet or JSON records have been inspected.

## Why this gate is necessary

The pinned [FAN-GHETS24 v2 Zenodo release](https://zenodo.org/records/13692267) is a **multipart ZIP**, not 72 independently readable samples. Its 72 files are 71 numbered parts (`fan-ghets24.z01` through `.z71`, each 262,144,000 bytes) and the terminal `fan-ghets24.zip` (36,719,241 bytes), totalling **18,648,943,241 bytes**. Zenodo lists these as one 18.65-GB dataset. The release instructions require joining/rebuilding the ZIP with `zip -FF fan-ghets24.zip --out fan-ghets24-combined.zip` before extraction. Downloading only the final `.zip` is **not a valid extraction plan**.

The published paper [Hutchins et al., Scientific Data 2025](https://doi.org/10.1038/s41597-025-05560-1) describes paired `example_host_data_srID.parquet`/`.json` records and source code at [Southampton GitLab](https://git.soton.ac.uk/ch1u20/fan-ghets24/). But no individual Parquet/JSON files are listed for direct download in the v2 Zenodo record.

## Run on Google Colab CPU (no PC research software)

```python
!wget -q -O /content/fan_ghets24_preflight.py https://raw.githubusercontent.com/itsCodeBakery/trustworthy-fanet-research/main/scripts/fan_ghets24_preflight.py
!python /content/fan_ghets24_preflight.py
```

Upload the saved `/content/fan_ghets24_preflight.json` to the conversation or paste the printed output.

The script contacts the **official Zenodo API** and optionally the authors' GitLab public repository API. It checks release version, exact 72 expected keys, byte counts and the published MD5s of the first and final split parts; and it reports Colab free disk space. A failed or rate-limited network request is clearly marked **NETWORK_UNAVAILABLE**, not silently deemed verified. No download of the 18.65-GB archive occurs.

## Decision after preflight

- **If manifest differs:** stop and investigate changed record metadata; do not mix v1 with v2.
- **If free temporary disk is low:** use persistent cloud Linux storage, not a short-lived Colab filesystem. Rebuilding a combined archive requires roughly another copy of compressed data, and extraction adds unknown space.
- **If a genuine small public sample is found in the author's public source repository:** record its URL, hashes, versions and relationship to v2 first; inspect it before paying the full transfer cost.
- **If no standalone official sample exists:** obtain all 72 v2 parts onto persistent cloud storage, MD5-verify each piece, rebuild, list extracted metadata safely, and inspect one real Parquet/JSON pair. This is a **later stage**, not performed by this preflight.

**Scientific criteria before training:** exact time order; local observation versus privileged attack metadata; available monitoring signals; stable simulation/run grouping; labels and attacks kept out of model inputs. Never invent fields from the descriptive journal article.
