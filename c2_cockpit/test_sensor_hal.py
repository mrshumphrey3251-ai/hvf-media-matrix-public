# -*- coding: utf-8 -*-
import os, sys, unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HAL_DIR = os.path.join(REPO_ROOT, "chronos_core", "hal")
if HAL_DIR not in sys.path:
    sys.path.insert(0, HAL_DIR)

from chronos_sensor_hal import (
    SensorRegistry, BaseSensorDriver, SensorType, SensorCriticality, SensorSample
)

class TestChronosSensorHALPublic(unittest.TestCase):
    def setUp(self):
        self.registry = SensorRegistry()

    def test_public_types_available(self):
        self.assertIn("OPTICAL_PPG", [t.value for t in SensorType])
        self.assertIn("CLINICAL_LIFE_CRITICAL", [c.name for c in SensorCriticality])

    def test_registry_initialization(self):
        self.assertEqual(len(self.registry.list_registered_sensors()), 0)

if __name__ == "__main__":
    unittest.main()
