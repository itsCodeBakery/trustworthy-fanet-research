#!/usr/bin/env python3
"""Read-only dataset metadata, checksum and sample-schema audit. No downloads."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def hashes(path):
    md5, sha256 = hashlib.md5(), hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            md5.update(block)
            sha256.update(block)
    return {'md5': md5.hexdigest(), 'sha256': sha256.hexdigest()}


def check_inventory(manifest_path, root=None):
    obj = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    files = obj.get('files', [])
    if not files or len({f['key'] for f in files}) != len(files):
        raise ValueError('Empty inventory or duplicate keys')
    if any(int(f['size']) < 0 for f in files):
        raise ValueError('Negative file size')
    if any(not str(f['checksum']).startswith(('md5:', 'sha256:')) for f in files):
        raise ValueError('Missing or unsupported checksums')
    total = sum(int(f['size']) for f in files)
    if total != int(obj['total_bytes']):
        raise ValueError('Inventory byte sum differs from advertised total')
    report = {'record': obj['record'], 'files_listed': len(files),
              'total_bytes': total, 'metadata_only': root is None,
              'files_examined': 0, 'missing_files': [], 'integrity_mismatches': []}
    if root is not None:
        root = Path(root)
        for f in files:
            p = root / f['key']
            if not p.is_file():
                report['missing_files'].append(f['key'])
                continue
            report['files_examined'] += 1
            algo, expected = f['checksum'].split(':', 1)
            actual = hashes(p)[algo]
            if p.stat().st_size != int(f['size']) or actual.lower() != expected.lower():
                report['integrity_mismatches'].append(f['key'])
    return report


def inspect_csv(path, expected_md5=None, expected_sha256=None):
    path = Path(path)
    digest = hashes(path)
    if expected_md5 and digest['md5'] != expected_md5.lower():
        raise ValueError('CSV MD5 mismatch')
    if expected_sha256 and digest['sha256'] != expected_sha256.lower():
        raise ValueError('CSV SHA-256 mismatch')
    with path.open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        if not columns or len(columns) != len(set(columns)):
            raise ValueError('Missing/duplicate CSV headers')
        labels = [x for x in columns if x.lower() in {'label', 'class'}]
        counts = {c: Counter() for c in labels}
        seen = set()
        missing = 0
        duplicates = 0
        n = 0
        for row in reader:
            if None in row:
                raise ValueError('Malformed CSV row with extra fields')
            n += 1
            missing += sum(value is None or value == '' for value in row.values())
            key = tuple(row[c] for c in columns)
            if key in seen:
                duplicates += 1
            else:
                seen.add(key)
            for c in labels:
                counts[c][row[c]] += 1
    return {'file': path.name, 'bytes': path.stat().st_size, **digest,
            'rows': n, 'columns': columns, 'missing_cells': missing,
            'exact_duplicate_rows': duplicates,
            'label_counts': {c: dict(v) for c, v in counts.items()},
            'has_event_timestamp_column': any(c.lower() in
                {'time', 'timestamp', 'time_s', 'event_time', 'packet_timestamp'}
                for c in columns),
            'audit_scope': 'raw CSV values only; no simulation-family provenance inferred'}


def inspect_fan_pair(parquet_path, json_path):
    try:
        import pyarrow.parquet as pq
    except ImportError as ex:
        raise RuntimeError('pyarrow required for Parquet inspection') from ex
    meta = json.loads(Path(json_path).read_text(encoding='utf-8'))
    pf = pq.ParquetFile(parquet_path)
    return {'parquet_file': Path(parquet_path).name,
            'metadata_file': Path(json_path).name,
            'schema': str(pf.schema_arrow), 'row_count': pf.metadata.num_rows,
            'metadata_keys': sorted(meta.keys()),
            'sample_loaded': False, 'independent_mission_identity_verified': False,
            'warning': 'Metadata alone cannot prove monitoring sufficiency; exclude attack points from model features'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='mode', required=True)
    p = sub.add_parser('inventory')
    p.add_argument('manifest', type=Path)
    p.add_argument('--root', type=Path)
    p = sub.add_parser('csv')
    p.add_argument('path', type=Path)
    p.add_argument('--expected-md5')
    p.add_argument('--expected-sha256')
    p = sub.add_parser('fan-pair')
    p.add_argument('parquet', type=Path)
    p.add_argument('metadata', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.mode == 'inventory':
        result = check_inventory(args.manifest, args.root)
    elif args.mode == 'csv':
        result = inspect_csv(args.path, args.expected_md5, args.expected_sha256)
    else:
        result = inspect_fan_pair(args.parquet, args.metadata)
    body = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as fp:
            fp.write(body)
    print(body, end='')


if __name__ == '__main__':
    main()
