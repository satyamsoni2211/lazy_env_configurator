from lazy_env_configurator import BaseConfig, BaseEnv
from pathlib import Path
from unittest import TestCase


class TestInvalidEnv(TestCase):

    def test_invalid_env_file(self):
        with self.assertRaises(FileNotFoundError) as e:
            class InvalidEnv(BaseEnv):
                class Config(BaseConfig):
                    dot_env_path = Path(__file__).parent / "invalid_env_file.env"
        self.assertIn("File not found at", str(e.exception))
