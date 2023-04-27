import os
from pytest import raises
from pydantic.error_wrappers import ValidationError
from pathlib import Path
from unittest import TestCase
from lazy_env_configurator import BaseConfig, BaseEnv
from lazy_env_configurator.custom_warnings import EnvWarning


class TestInvalidEnv(TestCase):

    def test_eager_validation(self):
        with raises(ValidationError) as e:
            class ContainedEnv(BaseEnv):
                class Config(BaseConfig):
                    envs = ("FOO", "APP")
                    dot_env_path = Path(__file__).parent / ".env.contained"
                    contained = True
                    validations = {
                        "FOO": {
                            "required": True,
                            "type": str,
                        },
                        "APP": {
                            "required": True,
                            "type": str
                        }
                    }
                    eagerly_validate = True
        self.assertIsInstance(e.value, ValidationError)
        self.assertEqual(e.value.raw_errors[0].loc_tuple()[1], "APP")
