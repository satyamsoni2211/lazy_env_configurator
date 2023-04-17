## LAZY_ENV_CONFIGURATOR

---

![Github Builds](https://img.shields.io/github/actions/workflow/status/satyamsoni2211/lazy_env_configurator/python-app.yml?style=plastic)

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

### How to use

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
>>>BaseConfig.instance.APP
```

Every class, subclassed from `BaseEnv` would expose `.instance` attribute which will be instance of the subclass. This instance can be used to access all the attributes on the class.

> For simplicity, `metaclass` pre-initialises created class, so to make it behave as singleton.

### How this works ?

---

`lazy_env_configurator` uses `descriptors` under the hood to dynamically populate env variables as attributes, thus making them available on demand, `Lazily`.
