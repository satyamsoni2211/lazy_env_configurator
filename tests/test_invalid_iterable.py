from lazy_env_configurator import BaseConfig, BaseEnv
from pathlib import Path
from unittest import TestCase


class TestInvalidIterableEnv(TestCase):

    def test_invalid_iterable_env(self):
        with self.assertRaises(TypeError) as e:
            class InvalidEnv(BaseEnv):
                class Config(BaseConfig):
                    envs = ('dev')
        self.assertIsInstance(e.exception, TypeError)
        self.assertIn("envs should be an iterable", str(e.exception))
