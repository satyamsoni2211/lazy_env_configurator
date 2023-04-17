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

    def test_empty_contained(self):
        with warns(EnvWarning) as w:
            class ContainedEnv(BaseEnv):
                class Config(BaseConfig):
                    envs = ("FOO", "APP")
                    contained = True
        message_ = w.list[0].message
        self.assertIsInstance(message_, EnvWarning)
        self.assertEqual(str(message_), ('\'Cannot Contain, No env variables found in dot env or no'
                         ' dot env file present or specified. This option should be used'
                                         ' exclusively with the .env files. \''))
