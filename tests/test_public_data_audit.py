"""Smoke tests on synthetic fixtures only, not reported experiments."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.verify_public_data import hashes, check_inventory, inspect_csv


class TestPublicDataAudit(unittest.TestCase):
    def test_inventory_records_and_checksums(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / 'a.bin').write_bytes(b'example')
            dig = hashes(base / 'a.bin')
            inv = {'record': 123, 'files': [{'key': 'a.bin', 'size': 7,
                    'checksum': 'md5:' + dig['md5']}], 'total_bytes': 7}
            p = base / 'inventory.json'
            p.write_text(json.dumps(inv))
            self.assertTrue(check_inventory(p)['metadata_only'])
            result = check_inventory(p, base)
            self.assertEqual(result['files_examined'], 1)
            self.assertEqual(result['integrity_mismatches'], [])
            (base / 'a.bin').write_bytes(b'altered')
            self.assertEqual(check_inventory(p, base)['integrity_mismatches'], ['a.bin'])

    def test_csv_hash_labels_duplicates_and_missing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'tiny.csv'
            with p.open('w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['FlowID', 'label', 'score'])
                w.writerow(['1', 'Normal', '1'])
                w.writerow(['1', 'Normal', '1'])
                w.writerow(['2', 'Attack', ''])
            result = inspect_csv(p, expected_sha256=hashes(p)['sha256'])
            self.assertEqual(result['rows'], 3)
            self.assertEqual(result['exact_duplicate_rows'], 1)
            self.assertEqual(result['missing_cells'], 1)
            self.assertEqual(result['label_counts']['label'], {'Normal': 2, 'Attack': 1})
            with self.assertRaises(ValueError):
                inspect_csv(p, expected_sha256='0' * 64)

    def test_reject_duplicate_inventory_keys(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'inv.json'
            p.write_text(json.dumps({'record': 1, 'files': [
                {'key': 'a', 'size': 0, 'checksum': 'md5:abc'},
                {'key': 'a', 'size': 0, 'checksum': 'md5:abc'}],
                'total_bytes': 0}))
            with self.assertRaises(ValueError):
                check_inventory(p)


if __name__ == '__main__':
    unittest.main()
