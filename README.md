## LAZY_ENV_CONFIGURATOR

---

![Github Builds](https://img.shields.io/github/actions/workflow/status/satyamsoni2211/lazy_env_configurator/python-app.yml?style=plastic)
[![codecov](https://codecov.io/gh/satyamsoni2211/lazy_env_configurator/branch/main/graph/badge.svg?token=9C55EA99PF)](https://codecov.io/gh/satyamsoni2211/lazy_env_configurator)
![Language Counts](https://img.shields.io/github/languages/count/satyamsoni2211/lazy_env_configurator)
![Version](https://img.shields.io/pypi/v/lazy-env-configurator)
![License](https://img.shields.io/github/license/satyamsoni2211/lazy_env_configurator)

A utility library for Dynamic Config class generation. Now no more repeated boilerplate code...

Before `lazy_env_configurator`, config classes used to be created as below.

```python
    class BaseConfig:
        APP = os.environ.get("APP")
        APP_ENV = os.environ.get("APP_ENV")

        # authentication related configuration
        # DB Credentials
        DB_USERNAME = os.environ.get("DB_USERNAME")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = os.environ.get("DB_PORT")
        DB_NAME = os.environ.get("DB_NAME")
        DB_DRIVER = os.environ.get("DB_DRIVER")
```

This use to require a lot of boiler plate and redundant code With `lazy_env_configurator` this can be reduced to below:

```python
from lazy_env_configurator import BaseEnv, BaseConfig as Config_
class BaseConfig(BaseEnv):
    class Config(Config_):
        envs = ('APP',
        'APP_ENV',
        'DB_USERNAME',
        'DB_PASSWORD',
        'DB_PASSWORD',
        'DB_HOST',
        # defaults
        ('DB_PORT',3306),
        'DB_NAME',
        'DB_DRIVER'
        )
```

### Benefits of using `lazy_env_configurator` over Normal classes

---

- Low memory footprint.
- Lazily evaluates environment variable and only loads them when used.
- Once loaded, env variables are cached.
- Get defaults populated, in case of missing `env` variables.
- env attributes can be overridden easily.
- classes expose `instance` attribute preventing need to initialization and making it behave singleton.
- Loads `.env` files by default so you only need to focus on essentials.
- Self Contained Objects if you do not want to sanatise global env variables. `contained` attribute.

### Components

---

- `BaseConfig`: Main Config class for library. This changes behavior of the container class.

  - `envs`: `List` or `Tuple` of `env` variable to be populated as attributes in container class. Elements of iterable can be a `string` or `tuple` with first element as attribute name and second as `default`, second element Defaults to `None`. Eg:

  ```python
  class Config(Config_):
        envs = ('APP',
        'APP_ENV',
        'DB_USERNAME',
        'DB_PASSWORD',
        'DB_PASSWORD',
        'DB_HOST',
        # defaults
        ('DB_PORT',3306),
        'DB_NAME',
        'DB_DRIVER'
        )
  ```

  - `dot_env_path`: Path to `.env` file. This can be a string or `pathlib.Path` object. defaults to `None`. Eg:

  ```python
  class Config(Config_):
        dot_env_path = Path(__file__).parent/'.env'
  ```

  - `contained`: This variable is responsible for behaviour of the container. If this is set to `False`, all the `env` variables read from `.env` file would be populated to `os.environ` and available globally. If this is set to `True`, environment variables would only be contained in the container itself. This would help to create configuration containers with different env settings. It `contained` is set to true and no `.env` file is present, it raises `EnvWarning` and fallback to Environment variables. Eg:

  ```python
  class Config(BaseConfig):
        envs = ("FOO", "APP")
        dot_env_path = Path(__file__).parent / ".env.contained"
        contained = True
  ```

- `BaseEnv`: This class will be used as a `Base Class` for all the containers. It uses `EnvMeta` as metaclass to populate `env` variables as attributes on Container Class. Eg:

  ```python
  from lazy_env_configurator import BaseEnv, BaseConfig as Config_
  class BaseConfig(BaseEnv):
      class Config(Config_):
          envs = ('APP',
          'APP_ENV',
          'DB_USERNAME',
          'DB_PASSWORD',
          'DB_PASSWORD',
          'DB_HOST',
          # defaults
          ('DB_PORT',3306),
          'DB_NAME',
          'DB_DRIVER'
          )
  ```

  > Note: `Config` class is optional. If not provided, it will not load any env variables.
  > `Config` class won't be available as an attribute on the child class.

- `EnvMeta`: Metaclass for populating env variables
  as class attributes to the child class.
  if the child class has a Config class, it will
  be used to populate the env variables.

  by default, the env variables are populated on first access
  and cached for subsequent access. This can be overriden by
  setting the value on the instance.

  if the env variable is not set, it uses the default value provided.

  This class also initializes the instance of the child class and
  make it available as `instance` attribute on the child class. So it can be accessed as
  `ChildClass.instance`.

  ```python
  Example:

  class ABC(BaseEnv):
    def generate_uri(self):
        return f'{self.DB_HOST}:{self.DB_PORT}'
    class Config(BaseConfig):
        envs = ('dev', ('test', 'test_value'),
                'prd', 'DB_HOST', 'DB_PORT')
        dot_env_path = Path(__file__).parent / '.env.test'

    >>> # access env variables
    >>> ABC.instance.dev
    >>> ABC.instance.test
    >>> ABC.instance.prd
  ```

### How to use

---

Let us refer below example:

```python
from lazy_env_configurator import BaseEnv, BaseConfig as Config_
class BaseConfig(BaseEnv):
    class Config(Config_):
        envs = ('APP',
        'APP_ENV',
        'DB_USERNAME',
        'DB_PASSWORD',
        'DB_PASSWORD',
        'DB_HOST',
        # defaults
        ('DB_PORT',3306),
        'DB_NAME',
        'DB_DRIVER'
        )
```

We can now use `BaseConfig` class create as below.

```python
>>> BaseConfig.instance.APP
```

Every class, subclassed from `BaseEnv` would expose `.instance` attribute which will be instance of the subclass. This instance can be used to access all the attributes on the class.

> For simplicity, `metaclass` pre-initialises created class, so to make it behave as singleton.

### How this works ?

---

`lazy_env_configurator` uses `descriptors` under the hood to dynamically populate env variables as attributes, thus making them available on demand, `Lazily`.
