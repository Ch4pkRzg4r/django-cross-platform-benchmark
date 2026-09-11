"""Verify v368 publication integrity without repeating thesis analyses."""
from pathlib import Path
import csv,hashlib,json,base64,gzip
r=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((r/'MANIFEST_V368_SHA256.csv').open(newline='')))
assert len({x['path'] for x in rows})==len(rows)
for x in rows:
    b=(r/x['path']).read_bytes()
    assert len(b)==int(x['bytes']),x['path']
    assert hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
c=json.loads((r/'documentation/v368_chapter2_correction_record.json').read_text())
assert c['live_endnote']==dict(citation_fields=225,bibliography_fields=1,distinct_records=115,source_use_links=256)
assert set(c['metadata_corrections'])=={'12','13','14','19','41','89','90','96','107','111'}
assert c['computational_release']=='v367'
assert hashlib.sha256((r/'data/canonical/master_runs.csv').read_bytes()).hexdigest()==c['canonical_sha256']
encoded=''.join((r/'analysis/v330-payload'/f'payload_{i:02d}.b64').read_text(encoding='ascii').strip() for i in range(1,6))
assert hashlib.sha256(gzip.decompress(base64.b64decode(encoded))).hexdigest()==c['frozen_v330_sha256']
assert 'PENDING' in c['whole_thesis_verdict']
print('PASS v368 manifest, correction-record invariants, canonical and frozen source identities')
