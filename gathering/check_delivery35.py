#!/usr/bin/env python3
"""Offline structural checks; no independent visual or functional certification."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

from check_delivery import Gallery, jpeg_dimensions, png_dimensions


def main():
    wall = Path('artifacts/gathering/wall-v15.png').read_bytes()
    assert wall == Path('artifacts/gathering/wall.png').read_bytes()
    assert png_dimensions(wall) == (1254, 1254)
    assert wall[24:26] == bytes((8, 2))
    digest = hashlib.sha256(wall).hexdigest()
    jpg = Path('dist/gathering/35.jpg').read_bytes()
    assert jpeg_dimensions(jpg) == (512, 512) and len(jpg) < 100000
    record = json.loads(Path('dist/gathering/35.json').read_text())
    assert set(record) == {'name', 'image', 'attributes'}
    assert record['image'] == 'https://api.imd.fun/artifacts/' + digest
    attrs = {a['trait_type']: a['value'] for a in record['attributes']}
    assert set(attrs) == {'Cave', 'Wall', 'Number', 'Left behind', 'Meaning', 'One thing'}
    assert len(record['attributes']) == 6
    assert attrs['Cave'] == 'Ice' and attrs['Wall'] == 'Gathering'
    assert type(attrs['Number']) is int and attrs['Number'] == 35
    assert attrs['One thing'] == 'Gathering'
    assert json.loads(Path('dist/goals.json').read_text()) == [
        {'line': i, 'goal': Path(f'line-{i}/GOAL.md').read_text().strip()} for i in range(1, 5)]

    content = Path('dist/index.html').read_text()
    gallery = Gallery(content)
    records = {p.relative_to('dist').as_posix(): json.loads(p.read_text())
               for p in Path('dist').glob('*/[0-9][0-9].json')}
    assert len(content.encode()) < 100000
    assert len(gallery.records) == len(records) == 175
    assert set(gallery.records) == set(records)
    assert len(gallery.images) == 75
    assert not set(gallery.tags) & {'script', 'iframe', 'link'}
    assert all(re.fullmatch(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', src)
               for src in gallery.images)
    for href in gallery.links:
        if href.startswith('#'):
            assert f'id="{href[1:]}"' in content
        elif not href.startswith('https://'):
            assert (Path('dist') / href).is_file(), href
    for name in ('gathering', 'line-1', 'line-2', 'line-3', 'line-4'):
        painted = [key for key in gallery.records if key.startswith(name+'/')
                   and records[key]['name'] != 'Not painted yet']
        assert painted == sorted(painted, reverse=True)
        for n in range(2, 22):
            p = Path('dist', name, f'{n:02}.json')
            assert json.loads(p.read_text()) == {
                'name': 'Not painted yet',
                'image': 'https://api.imd.fun/artifacts/b5e794cb2c70bd232230e389707698c69c2080786d606a13b39f9315c9a90799',
                'attributes': [{'trait_type': 'Cave', 'value': 'Ice'}]}
            assert not p.with_suffix('.jpg').exists()

    baseline = json.loads(Path('gathering/scope-before35.json').read_text())
    actual = {str(p) for i in range(1, 5) for p in Path(f'line-{i}').rglob('*') if p.is_file()}
    assert actual == set(baseline)
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in baseline.items())
    paths = [f'line-{i}' for i in range(1, 5)] + [f'dist/line-{i}' for i in range(1, 5)]
    assert not subprocess.run(['git', 'diff', 'HEAD', '--', *paths], capture_output=True, check=True).stdout
    changed = subprocess.run(['git', 'diff', '--name-only', 'HEAD'],
                             capture_output=True, text=True, check=True).stdout.splitlines()
    added = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    for name in set(changed + added):
        assert name.split('/')[0] in ('gathering', 'shared', 'dist'), name
        assert Path(name).is_file() and Path(name).stat().st_size < 100000, name
    scout = Path('line-2/tools/csv-key-scout/scout.py').read_text().replace(
        "sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'csv-reconcile'))\n", '')
    assert scout == Path('shared/http-evidence/key_candidates.py').read_text()
    assert Path('shared/http-evidence/reconcile.py').read_bytes() == Path('line-2/tools/csv-reconcile/reconcile.py').read_bytes()

    tests = json.loads(Path('gathering/test-runs35.json').read_text())
    assert tests['ok'] and tests['line_tests'] == 548 and tests['shared_tests'] == 105
    assert tests['gathering_tests'] == 8 and tests['sources_unchanged_after_checks']
    covered, trials = set(), 0
    for name in ('integration-checks35', 'later-checks35', 'payload-checks35', 'current-checks35'):
        report = json.loads(Path('gathering', name+'.json').read_text())
        assert report['ok']
        trials += len(report['results'])
        for row in report['results']:
            assert row['passed']
            for part in row['command']:
                if part.startswith('line-') and part.endswith('.py'):
                    covered.add(str(Path(part).parent))
    assert trials == 132
    assert covered == {str(p) for p in Path('.').glob('line-*/tools/*') if p.is_dir()}
    image = json.loads(Path('gathering/image-checks35.json').read_text())
    assert image['png']['sha256'] == digest
    assert image['preservation']['changed_pixels'] == 2461
    assert image['preservation']['outside_rectangle_changed_pixels'] == 0
    assert image['visual_review_completed'] and image['unmet_visual_requirements'] == []
    assert Path('gathering/COINS.md').read_text().splitlines()[0] == 'none'
    for name in ('coin-order.json', 'deploy-order.json'):
        assert not Path('gathering', name).exists()
    result = dict(ok=True, png=dict(format='PNG', mode='RGB', dimensions=[1254,1254], sha256=digest),
                  jpeg=dict(format='JPEG', dimensions=[512,512], bytes=len(jpg)),
                  gallery_records=175, painted_previews=75, placeholders=100,
                  gallery_bytes=len(content.encode()), cli_trials=trials, tools_tried=len(covered),
                  line_paths_unchanged=True, scope_ok=True, unmet_visual_requirements=[])
    Path('gathering/delivery-checks35.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
