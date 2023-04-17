import os
from pathlib import Path
from pytest import raises
from unittest import TestCase
from lazy_env_configurator import BaseEnv, BaseConfig

os.environ.setdefault('prd', 'prd_value')


class ABC(BaseEnv):

    def generate_uri(self):
        return f'{self.DB_HOST}:{self.DB_PORT}'

    class Config(BaseConfig):
        envs = ('dev', ('test', 'test_value'), 'prd', 'DB_HOST', 'DB_PORT')
        dot_env_path = Path(__file__).parent / '.env.test'


class EmptyBase(BaseEnv):
    class Config(BaseConfig):
        ...


class TestEnvMeta(TestCase):
    def setUp(self) -> None:
        self.t_ = ABC.instance
        self.e_ = EmptyBase.instance

    def test_dev(self):
        self.assertIsNone(self.t_.dev)
        self.t_.dev = "wow"
        # checking overwriting
        self.assertEqual(self.t_.dev, 'wow')

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
