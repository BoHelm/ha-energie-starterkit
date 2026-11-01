"""Synthetic release checks, not tests of a running HA installation."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('releasecheck', ROOT / 'scripts' / 'check_release.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.demo = json.loads((ROOT / 'config' / 'demo.json').read_text())

    def categories(self, text):
        return {name for name, _ in c.findings(text)}

    def test_whole_package(self):
        self.assertEqual(c.check(), [])

    def test_demo_is_synthetic(self):
        self.assertTrue(self.demo['example_only'])
        self.assertEqual(c.validate_config(self.demo), [])

    def test_template_has_no_plant_values(self):
        d = json.loads((ROOT / 'config' / 'anlage.vorlage.json').read_text())
        self.assertEqual(c.validate_config(d), [])
        self.assertTrue(all(v is None for v in d['hardware'].values()))

    def test_boolean_is_not_integer(self):
        self.demo['permissions']['device_writes'] = 0
        self.assertTrue(c.validate_config(self.demo))

    def test_no_permission_expansion(self):
        self.demo['permissions']['device_writes'] = True
        self.assertTrue(c.validate_config(self.demo))

    def test_bad_fraction(self):
        for v in (1.1, -0.1, True, float('inf'), '0.9'):
            d = copy.deepcopy(self.demo)
            d['assumptions']['pv_usable_fraction'] = v
            self.assertTrue(c.validate_config(d))

    def test_size_consistency(self):
        self.demo['hardware']['battery_usable_kwh'] = 99
        self.assertTrue(c.validate_config(self.demo))

    def test_duplicate_source(self):
        self.demo['sources']['pv_power'] *= 2
        self.assertTrue(c.validate_config(self.demo))

    def test_invalid_snapshot_time(self):
        self.demo['assumptions']['forecast_snapshot_local_time'] = '25:01'
        self.assertTrue(c.validate_config(self.demo))

    def test_leak_patterns(self):
        fixtures = {
            'email': 'sample' + chr(64) + 'example.invalid',
            'ipv4': '.'.join(map(str, (10, 2, 3, 4))),
            'mac': ':'.join(['aa', 'bb', 'cc', 'dd', 'ee', 'ff']),
            'hardware_identifier': '12345' * 3,
            'coordinate_pair': '12.' + '34567, 34.' + '56789',
            'coordinate_assignment': '"latitude": ' + '12.34',
            'secret': 'ghp_' + 'X' * 24,
            'local_path': '/' + 'Users/' + 'sample/private.txt',
            'non_demo_entity': 'sensor.' + 'private_identifier',
        }
        for name, text in fixtures.items():
            with self.subTest(name=name):
                self.assertIn(name, self.categories(text))

    def test_no_match_content_in_report(self):
        marker = 'sample' + chr(64) + 'example.invalid'
        self.assertNotIn(marker, repr(c.findings(marker)))

    def test_demo_sources_allowed(self):
        self.assertEqual(c.findings('sensor.demo_wp_innen_energie'), [])

    def test_offset_module_is_disabled(self):
        self.assertFalse(self.demo['modules']['heat_pump_offset_control'])
        self.demo['modules']['heat_pump_offset_control'] = True
        self.assertTrue(c.validate_config(self.demo))

    def test_offset_entity_privacy(self):
        self.assertEqual(c.findings('climate.demo_wp_offset'), [])
        self.assertEqual(c.findings('climate.set_temperature'), [])
        self.assertIn('non_demo_entity', self.categories('climate.' + 'private_offset'))

    def test_official_links_allowed(self):
        self.assertEqual(c.findings('https://www.home-assistant.io/integrations/'), [])

    def test_unresolved_is_not_zero(self):
        self.demo['assumptions']['pv_usable_fraction'] = 0
        self.assertEqual(c.validate_config(self.demo), [])


if __name__ == '__main__':
    unittest.main()
