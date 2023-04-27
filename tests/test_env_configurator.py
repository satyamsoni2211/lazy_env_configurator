import os
from pathlib import Path
from pytest import raises
from unittest import TestCase
from pydantic.errors import IntegerError
from pydantic.error_wrappers import ValidationError
from lazy_env_configurator import BaseEnv, BaseConfig

os.environ.setdefault('prd', 'prd_value')


class ABC(BaseEnv):

    def generate_uri(self):
        return f'{self.DB_HOST}:{self.DB_PORT}'

    class Config(BaseConfig):
        envs = ('dev', ('test', 'test_value'),
                ('test_int', 'foobar'), 'prd', 'DB_HOST', 'DB_PORT')
        dot_env_path = Path(__file__).parent / '.env.test'
        validations = {
            'dev': {
                'alias': 'dev',
                'type': str,
                'required': True,
                'min_length': 5
            },
            'DB_HOST': {
                'required': True,
                'type': str,
                'min_length': 5
            },
            'test_int': {
                'required': True,
                'type': int,
            }
        }


class EmptyBase(BaseEnv):
    class Config(BaseConfig):
        ...


class TestEnvMeta(TestCase):
    def setUp(self) -> None:
        self.t_ = ABC.instance
        self.e_ = EmptyBase.instance

    def test_invalid_env_dev(self):
        with raises(ValidationError) as e:
            self.assertIsNone(self.t_.dev)
        self.assertIsInstance(e.value, ValidationError)

    def test_invalid_env_test_int_default(self):
        with raises(ValidationError) as e:
            self.assertIsNone(self.t_.test_int)
        self.assertIsInstance(e.value, ValidationError)
        self.assertIsInstance(e.value.raw_errors[0].exc, IntegerError)
        self.assertEqual(e.value.raw_errors[0].loc_tuple()[1], 'test_int')
        self.assertIn("value is not a valid integer", str(e.value))

    def test_invalid_dev_value(self):
        with raises(ValidationError) as e:
            self.t_.dev = "wow"
            # checking overwriting
            self.assertEqual(self.t_.dev, 'wow')
        self.assertIsInstance(e.value, ValidationError)
        self.assertIn("ensure this value has at least 5 characters", str(e.value))

    def test_valid_dev_value(self):
        self.t_.dev = "wowlength"
        # checking overwriting
        self.assertEqual(self.t_.dev, 'wowlength')

    def test_test(self):
        self.assertEqual(self.t_.test, 'test_value')

    def test_prd(self):
        self.assertEqual(self.t_.prd, 'prd_value')

    def test_no_config_class(self):
        self.assertIsNone(getattr(self.t_, "Config", None))

    def test_generate_uri(self):
        self.assertEqual(self.t_.generate_uri(), 'localhost:1223')

    def test_env_from_file(self):
        self.assertEqual(self.t_.DB_HOST, 'localhost')
        self.assertEqual(self.t_.DB_PORT, '1223')

    def test_failure(self):
        with raises(AttributeError) as e:
            self.e_.test
        self.assertIsInstance(e.value, AttributeError)
