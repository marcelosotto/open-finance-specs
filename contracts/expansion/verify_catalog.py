"""Offline integrity verification for the pinned OF catalogue (requires PyYAML)."""
import hashlib
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
catalog = json.loads((ROOT / 'contracts/expansion/catalog.json').read_text(encoding='utf-8'))
rows = json.loads((ROOT / 'contracts/expansion/sources/official-table.json').read_text(encoding='utf-8'))
active = {(r['groupAcronym'], r['api'], v['version'], v['status']) for r in rows for v in r['versions'] if v['status'] in {'Current', 'Deprecated'}}
actual = {(c['domain'], c['family'], c['specificationVersion'], c['versionStatus']) for c in catalog['contracts']}
assert actual == active, (active - actual, actual - active)
keys = set()
count = 0
for c in catalog['contracts']:
    data = (ROOT / c['localPath']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == c['sha256'], c['id']
    spec = yaml.safe_load(data)
    assert str(spec['info']['version']) == c['specificationVersion'] == c['advertisedVersion']
    pairs = {(method.upper(), path, op.get('operationId')) for path, item in spec['paths'].items() for method, op in item.items() if method.lower() in {'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'}}
    assert pairs == {(o['method'], o['path'], o['operationId']) for o in c['operations']}, c['id']
    for op in c['operations']:
        assert op['unitKey'] not in keys
        keys.add(op['unitKey'])
        count += 1
for source in catalog['sources']:
    assert hashlib.sha256((ROOT / source['localPath']).read_bytes()).hexdigest() == source['sha256']
legacy = json.loads((ROOT / 'contracts/manifest.json').read_text(encoding='utf-8-sig'))
for item in legacy:
    assert hashlib.sha256((ROOT / 'contracts/open-finance' / item['name']).read_bytes()).hexdigest() == item['sha256']
assert len(actual) == catalog['summary']['activeContracts'] == 35
assert count == catalog['summary']['activeOperations'] == 143
assert len(keys) == count
print(f'PASS: {len(actual)} active contracts, {count} unique operations, {len(catalog["sources"])} source hashes, {len(legacy)} legacy snapshots unchanged.')
