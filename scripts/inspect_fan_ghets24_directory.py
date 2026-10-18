#!/usr/bin/env python3
"""Safe FAN-GHETS24 v2 ZIP central-directory inspection (NO extraction).

Downloads ONLY the final 36,719,241-byte multipart-ZIP segment from official
Zenodo API links, validates its published MD5, and lists metadata using Python
zipfile. This does NOT download the other 71 volumes, read Parquet samples,
or prove that data samples can be extracted.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import requests

RECORD = 13692267
PART = "fan-ghets24.zip"
EXPECTED_SIZE = 36_719_241
EXPECTED_MD5 = "d922794f042ba3398949a02114ee0af4"
DEST = Path("/content/fan-ghets24.zip")
REPORT = Path("/content/fan_ghets24_zip_directory.json")


def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def choose_url(item):
    links = item.get("links", {})
    candidates = [
        links.get("content"), links.get("download"), links.get("self"),
        f"https://zenodo.org/records/{RECORD}/files/{PART}?download=1"
    ]
    for u in candidates:
        if isinstance(u, str) and u.startswith("https://"):
            # A metadata-only 'self' link is not the binary 'content' route.
            if "/api/records/" in u and "/content" not in u:
                continue
            return u
    raise RuntimeError("No HTTPS content link found for final ZIP part")


def verify_zenodo_item(record):
    if str(record.get("id")) != str(RECORD):
        raise RuntimeError("Unrecognized Zenodo record identity")
    files = record.get("files", [])
    parts = [x for x in files if x.get("key") == PART]
    if len(parts) != 1:
        raise RuntimeError("The terminal multipart-ZIP part was not found uniquely")
    item = parts[0]
    if item.get("size") != EXPECTED_SIZE:
        raise RuntimeError("Unexpected last-segment size; stop rather than download")
    if item.get("checksum", "").lower() != "md5:" + EXPECTED_MD5:
        raise RuntimeError("Unexpected published last-segment MD5")
    return choose_url(item)


def download_terminal_part(session, url, path):
    if path.exists():
        if path.stat().st_size != EXPECTED_SIZE or digest(path) != EXPECTED_MD5:
            raise RuntimeError("Existing destination file differs from pinned part; do not overwrite")
        return "existing_file_verified"
    temp = path.with_suffix(".zip.partial")
    if temp.exists():
        raise RuntimeError("Partial download found. Inspect it or remove explicitly and retry.")
    try:
        with session.get(url, stream=True, timeout=(15, 90)) as resp:
            resp.raise_for_status()
            announced = resp.headers.get("Content-Length")
            if announced is not None and int(announced) > EXPECTED_SIZE:
                raise RuntimeError("Announced payload exceeds expected file size")
            n = 0
            with temp.open("xb") as handle:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        n += len(chunk)
                        if n > EXPECTED_SIZE:
                            raise RuntimeError("Downloaded payload exceeds pinned file size")
                        handle.write(chunk)
        if temp.stat().st_size != EXPECTED_SIZE or digest(temp) != EXPECTED_MD5:
            raise RuntimeError("Downloaded final-part size or MD5 invalid")
        temp.replace(path)
        return "downloaded_and_verified"
    except Exception:
        if temp.exists():
            temp.unlink()
        raise


def read_directory(path):
    # ZIP central directory usually resides in the terminal part of a split ZIP.
    # zipfile can read entry metadata here; it cannot read early members' bytes.
    with ZipFile(path) as archive:
        infos = archive.infolist()
        if not infos:
            raise RuntimeError("No ZIP directory entries found")
        names = [entry.filename for entry in infos]
        files = [entry for entry in infos if not entry.is_dir()]
        parquet = [n for n in names if n.lower().endswith(".parquet")]
        jsons = [n for n in names if n.lower().endswith(".json")]
        paired_stems = set(n[:-8] for n in parquet) & set(n[:-5] for n in jsons)
        return {
            "archive_directory_entries": len(infos),
            "archived_regular_files": len(files),
            "total_uncompressed_bytes": sum(f.file_size for f in files),
            "total_uncompressed_gib": round(sum(f.file_size for f in files) / 2**30, 2),
            "parquet_entries": len(parquet),
            "json_entries": len(jsons),
            "paired_parquet_json_stems": len(paired_stems),
            "first_25_paths": names[:25],
            "example_pair_stems": sorted(paired_stems)[:10],
            "archive_contents_read_or_extracted": False,
        }


def main():
    with requests.Session() as session:
        response = session.get(f"https://zenodo.org/api/records/{RECORD}",
                               timeout=(15, 45), headers={"Accept": "application/json"})
        response.raise_for_status()
        url = verify_zenodo_item(response.json())
        provenance = download_terminal_part(session, url, DEST)
    try:
        inspection = read_directory(DEST)
        status = "ZIP_DIRECTORY_INSPECTED"
        issue = None
    except (BadZipFile, OSError, RuntimeError) as ex:
        inspection = {}
        issue = str(ex)
        status = "DIRECTORY_UNAVAILABLE_FROM_TERMINAL_PART"
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "record_id": RECORD,
        "source": f"https://zenodo.org/records/{RECORD}",
        "downloaded_only_terminal_part": True,
        "terminal_part_size": EXPECTED_SIZE,
        "terminal_part_md5": digest(DEST),
        "terminal_part_verification": provenance,
        "all_71_preceding_parts_downloaded": False,
        "original_data_parquet_samples_read": 0,
        "directory_error": issue,
        "directory": inspection,
        "warning": "Central-directory inspection is not sample validation and cannot establish run IDs or early-event semantics.",
    }
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print("Terminal ZIP part verified:", provenance)
    print("ZIP directory status:", status)
    if issue:
        print("Directory note:", issue)
    else:
        print("Entries:", inspection["archive_directory_entries"])
        print("Total uncompressed GiB:", inspection["total_uncompressed_gib"])
        print("Parquet / JSON:", inspection["parquet_entries"],
              "/", inspection["json_entries"])
        print("Paired stems:", inspection["paired_parquet_json_stems"])
        print("First paths:", *inspection["first_25_paths"][:8], sep="\n  ")
    print("Report:", REPORT)
    print("Do not attempt to read or extract data members from this final part alone.")


if __name__ == "__main__":
    main()
