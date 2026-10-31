#!/usr/bin/env python3
"""Check this neutral publication package. No network access and no HA writes."""
from pathlib import Path
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'README.md', 'AGENTS.md', 'LICENSE', 'CONTRIBUTING.md', '.gitignore',
    'prompts/MASTER-PROMPT.md', 'config/anlage.vorlage.json', 'config/demo.json',
    'scripts/check_release.py', 'tests/test_release.py',
    *{f'docs/{name}.md' for name in (
        '01-einrichtung', '02-sensoren-und-parameter', '03-module',
        '04-berechnungen', '05-datenqualitaet', '06-abnahme',
        '07-datenschutz', '08-betrieb', '09-status-und-grenzen', '10-referenzarchitektur')},
}
PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'ipv4': r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',
    'ipv6': r'(?i)(?<!\w)(?:[a-f0-9]{1,4}:){3,}[a-f0-9:]+',
    'mac': r'(?i)(?<!\w)(?:[a-f0-9]{2}[:-]){5}[a-f0-9]{2}(?!\w)',
    'hardware_identifier': r'(?i)\b(?:[a-f0-9]{12}|\d{10,}|[a-f0-9]{24,})\b',
    'secret': r'\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{12,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\beyJ[A-Za-z0-9_-]{12,}\.',
    'local_path': r'(?:/Users/|/home/)[A-Za-z0-9._-]+/',
    'remote_home': r'https?://[^\s/]+\.(?:ui\.nabu\.casa|duckdns\.org)',
    'coordinate_pair': r'(?<!\d)[+-]?\d{1,2}\.\d{4,}\s*,\s*[+-]?\d{1,3}\.\d{4,}(?!\d)',
    'coordinate_assignment': r'(?i)["\']?(?:latitude|longitude|gps_latitude|gps_longitude)["\']?\s*[:=]\s*[+-]?\d',
    'map_location_url': r'https?://\S*(?:maps\S*[?&](?:q|ll)=|[?&](?:lat|lon|latitude|longitude)=)',
}
COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}
ENTITY = re.compile(r'\b(?:sensor|binary_sensor|number|input_number|input_boolean|device_tracker|person|notify)\.[a-z0-9_]+\b')
ARRAY_ROLES = {'pv_power', 'pv_energy', 'wp_power', 'bev_power'}


def findings(text):
    """Return categories/line numbers, deliberately never matched private text."""
    out = [(name, text.count('\n', 0, m.start()) + 1)
           for name, pattern in COMPILED.items() for m in pattern.finditer(text)]
    out += [('non_demo_entity', text.count('\n', 0, m.start()) + 1)
            for m in ENTITY.finditer(text) if '.demo_' not in m.group()]
    return out


def validate_config(data):
    """Validate public questionnaire shape, types and conservative defaults."""
    errors = []
    top = {'format_version', 'example_only', 'timezone', 'hardware', 'modules', 'sources', 'assumptions', 'permissions'}
    if set(data) != top:
        return ['unexpected or missing top-level fields']
    if type(data['format_version']) is not int or data['format_version'] != 1:
        errors.append('format_version must be integer 1')
    if type(data['example_only']) is not bool:
        errors.append('example_only must be boolean')
    if data['timezone'] is not None and not isinstance(data['timezone'], str):
        errors.append('timezone must be text or null')
    for group in ('modules', 'permissions'):
        if not isinstance(data[group], dict) or any(type(v) is not bool for v in data[group].values()):
            errors.append(group + ' must contain booleans')
    if data['permissions'] != {'device_writes': False, 'community_transmission': False, 'notifications': False}:
        errors.append('public permission defaults must remain disabled')
    for key, value in data['hardware'].items():
        if key.endswith(('_kwh', '_kwp')) and value is not None:
            if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                errors.append('invalid hardware size: ' + key)
    if data['hardware']['battery_nominal_kwh'] is not None and data['hardware']['battery_usable_kwh'] is not None:
        if data['hardware']['battery_usable_kwh'] > data['hardware']['battery_nominal_kwh']:
            errors.append('usable battery energy exceeds nominal energy')
    for role, value in data['sources'].items():
        if role in ARRAY_ROLES:
            if not isinstance(value, list):
                errors.append('source role must be an array: ' + role)
                continue
            values = value
        else:
            values = [] if value is None else [value]
        if len(values) != len(set(v for v in values if isinstance(v, str))):
            errors.append('duplicate or invalid source in role: ' + role)
        if any(not isinstance(v, str) or not re.fullmatch(r'[a-z_]+\.demo_[a-z0-9_]+', v) for v in values):
            errors.append('public source must use synthetic demo naming: ' + role)
    for key in ('pv_usable_fraction', 'temporal_uncertainty_fraction'):
        value = data['assumptions'][key]
        if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1):
            errors.append('invalid fraction: ' + key)
    when = data['assumptions']['forecast_snapshot_local_time']
    if when is not None and not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', str(when)):
        errors.append('invalid snapshot local time')
    if not data['example_only']:
        # The distributable questionnaire has no real values or sources filled in.
        if data['timezone'] is not None or any(v is not None for v in data['hardware'].values()):
            errors.append('questionnaire must not contain a real plant profile')
        if any(v not in (None, []) for v in data['sources'].values()):
            errors.append('questionnaire must not contain real source assignments')
        if any(v not in (None, []) for v in data['assumptions'].values()):
            errors.append('questionnaire assumptions must remain unresolved')
    return errors


def check(root=ROOT):
    errors = []
    actual = set()
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in ('.git', '__pycache__') for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append(f'{rel}: symlink is not permitted')
            continue
        if not path.is_file():
            continue
        name = rel.as_posix()
        actual.add(name)
        if name not in EXPECTED:
            errors.append(f'{name}: file not on explicit publication allowlist')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{name}: expected UTF-8 text only')
            continue
        errors.extend(f'{name}:{line}: {category}' for category, line in findings(text))
        if path.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                dest = (path.parent / target.split('#', 1)[0]).resolve()
                if not dest.is_relative_to(root.resolve()) or not dest.is_file():
                    errors.append(f'{name}: missing or escaping relative link')
    errors.extend(f'{name}: missing file' for name in sorted(EXPECTED - actual))
    for name in ('anlage.vorlage.json', 'demo.json'):
        try:
            obj = json.loads((root / 'config' / name).read_text())
            errors.extend(f'config/{name}: {e}' for e in validate_config(obj))
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            errors.append(f'config/{name}: invalid configuration shape')
    return errors


if __name__ == '__main__':
    problems = check()
    if problems:
        print('\n'.join(problems))
        sys.exit(1)
    print(f'PASS: {len(EXPECTED)} allowlisted files; links, public templates and privacy patterns checked.')
    print('Manual content and Git-metadata review remains necessary. No HA installation was tested.')
