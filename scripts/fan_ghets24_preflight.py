#!/usr/bin/env python3
"""FAN-GHETS24 v2 cloud preflight: metadata only, NO dataset downloads."""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RECORD = 13692267
ZENODO = f"https://zenodo.org/api/records/{RECORD}"
GITLAB = ("https://git.soton.ac.uk/api/v4/projects/"
          "ch1u20%2Ffan-ghets24/repository/tree?per_page=100")
EXPECTED_TOTAL_BYTES = 18_648_943_241
CHUNK_BYTES = 262_144_000
FINAL_BYTES = 36_719_241
EXPECTED_KEYS = {f"fan-ghets24.z{i:02d}" for i in range(1, 72)} | {"fan-ghets24.zip"}
EXPECTED_MD5 = {
    "fan-ghets24.z01": "9a2bd2de582fafbd0774f2fc6a993d5b",
    "fan-ghets24.zip": "d922794f042ba3398949a02114ee0af4",
}


def retrieve(session, url):
    try:
        r = session.get(url, timeout=(12, 35), headers={"Accept": "application/json"})
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        return r.json(), None
    except (ValueError, requests.RequestException) as exc:
        return None, type(exc).__name__ + ": " + str(exc)[:240]


def manifest_audit(record):
    files = record.get("files")
    if not isinstance(files, list):
        return {"status": "INVALID", "problems": ["No files array in Zenodo response"]}
    keys = [item.get("key") for item in files]
    indexed = {item["key"]: item for item in files if isinstance(item.get("key"), str)}
    problems = []
    if str(record.get("id")) != str(RECORD):
        problems.append(f"Record ID differs: {record.get('id')!r}")
    if len(files) != 72 or len(indexed) != 72:
        problems.append(f"Expected 72 distinct files, found {len(files)} items / {len(indexed)} unique")
    if set(indexed) != EXPECTED_KEYS:
        problems.append("File-key set differs from v2 split-ZIP release")
    try:
        total = sum(int(f["size"]) for f in files)
        if total != EXPECTED_TOTAL_BYTES:
            problems.append(f"Total bytes changed: {total}")
        for key in EXPECTED_KEYS.intersection(indexed):
            should = FINAL_BYTES if key.endswith(".zip") else CHUNK_BYTES
            if int(indexed[key]["size"]) != should:
                problems.append(f"Size mismatch: {key}")
        for key, md5 in EXPECTED_MD5.items():
            if indexed.get(key, {}).get("checksum", "").lower() != "md5:" + md5:
                problems.append(f"Known MD5 mismatch: {key}")
    except (TypeError, ValueError, KeyError) as exc:
        problems.append("Invalid size fields: " + repr(exc))
        total = None
    # Zenodo may omit metadata.version even when the publication page labels
    # this exact immutable record v2. Identity + manifest checks are decisive;
    # the *absence* of optional version metadata is not a file mismatch.
    version = record.get("metadata", {}).get("version")
    if version is not None and version != "v2":
        problems.append(f"Unexpected explicit version field: {version!r}")
    return {
        "status": "VERIFIED_METADATA" if not problems else "MISMATCH",
        "version_reported": version,
        "version_field_optional_and_absent": version is None,
        "record_id_matches_pin": str(record.get("id")) == str(RECORD),
        "files_reported": len(files),
        "bytes_reported": total,
        "files_are_split_zip": True,
        "problems": problems,
        "direct_sample_parquet_available_in_record": any(
            str(k).lower().endswith((".parquet", ".json")) for k in keys
        ),
    }


def main():
    session = requests.Session()
    retry = Retry(total=2, backoff_factor=1.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    free = shutil.disk_usage("/content" if Path("/content").exists() else "/").free
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "stage": "METADATA_AND_CLOUD_CAPACITY_PREFLIGHT_ONLY",
        "record": RECORD,
        "official_record_url": "https://zenodo.org/records/13692267",
        "source_repo": "https://git.soton.ac.uk/ch1u20/fan-ghets24/",
        "public_dataset_bytes_downloaded": 0,
        "parquet_samples_inspected": 0,
        "local_runtime_free_gib": round(free / 2**30, 2),
        "archive_compressed_gib": round(EXPECTED_TOTAL_BYTES / 2**30, 2),
        "temporary_space_for_split_parts_plus_reconstructed_zip_gib": round(
            2 * EXPECTED_TOTAL_BYTES / 2**30, 2
        ),
        "important_space_warning": (
            "The estimated two-copy footprint excludes any extracted data, "
            "notebook caches and overhead. Do not download until extraction "
            "size, persistent storage and run-time quota are checked."
        ),
    }
    record, err = retrieve(session, ZENODO)
    result["zenodo_request_error"] = err
    result["manifest"] = manifest_audit(record) if record else {
        "status": "NETWORK_UNAVAILABLE", "problems": [err]
    }
    tree, tree_err = retrieve(session, GITLAB)
    result["gitlab_request_error"] = tree_err
    if isinstance(tree, list):
        result["gitlab_public_root_entries"] = [
            {"name": e.get("name"), "type": e.get("type")} for e in tree[:50]
        ]
        result["gitlab_tree_status"] = "ACCESSIBLE"
    else:
        result["gitlab_tree_status"] = "NOT_VERIFIED"
    target = Path("/content/fan_ghets24_preflight.json") if Path("/content").exists() else Path("fan_ghets24_preflight.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("FAN-GHETS24 v2 preflight — no dataset archive downloaded")
    print("Zenodo manifest:", result["manifest"]["status"])
    if result["manifest"].get("version_field_optional_and_absent"):
        print("Info: metadata.version is absent; published record page identifies pinned record as v2.")
    print("Manifest problems:", result["manifest"]["problems"])
    print("Colab free space (GiB):", result["local_runtime_free_gib"])
    print("Two-copy archive footprint before extraction (GiB):",
          result["temporary_space_for_split_parts_plus_reconstructed_zip_gib"])
    print("Authors' GitLab source tree API:", result["gitlab_tree_status"])
    print("Note: GitLab API HTTP 401 does not establish the browser-visible project is private.")
    if tree_err:
        print("Source-tree access issue:", tree_err)
    print("Report saved:", target)
    print("Next: share the JSON or printed summary; do NOT start the 18.65 GB download yet.")


if __name__ == "__main__":
    main()
