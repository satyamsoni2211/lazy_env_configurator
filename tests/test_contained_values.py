import os
from pytest import warns
from pathlib import Path
from unittest import TestCase
from lazy_env_configurator import BaseConfig, BaseEnv
from lazy_env_configurator.custom_warnings import EnvWarning


class ContainedEnv(BaseEnv):
    class Config(BaseConfig):
        envs = ("FOO", "APP")
        dot_env_path = Path(__file__).parent / ".env.contained"
        contained = True


class TestInvalidEnv(TestCase):
    def setUp(self) -> None:
        self.t_ = ContainedEnv.instance

    def test_contained_env_file(self):
        self.assertEqual(self.t_.FOO, "BAR")
        self.assertIsNone(self.t_.APP)

    def test_env(self):
        self.assertIsNone(os.getenv("FOO"))

    def test_is_contained(self):
        self.assertTrue(hasattr(self.t_, "__contained__"))
