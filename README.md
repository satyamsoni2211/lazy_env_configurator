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

  - `contained`: This variable is responsible for behaviour of the container. If this is set to `False`, all the `env` variables read from `.env` file would be populated to `os.environ` and available globally. If this is set to `True`, environment variables would only be contained in the container itself. This would help to create configuration containers with different env settings. It `contained` is set to true and no `.env` file is present, it will fallback to Environment variables. default `True`. Eg:

    ```python
    class Config(BaseConfig):
          envs = ("FOO", "APP")
          dot_env_path = Path(__file__).parent / ".env.contained"
          contained = True
    ```

  - `validations`: Dict of validations to be applied to the env variables.
    The key of the dict is the name of the env variable and the value is the validation options.
    The validation options are the same as the pydantic field info.

    > This is a dictionary of key as `environment Variables` and value as `lazy_env_configurator.validations:ValidationOptions`. These are all the arguments that are passed for [Field Customisations](https://docs.pydantic.dev/usage/schema/#field-customization). This supports auto completion.

    ```python
    class Abc(BaseEnv):
      class Config(BaseConfig):
          envs = ('dev', 'test')
          validations = {
              'dev': {
                  "alias": "dev",
                  "gt": 4,
                  "type": int,
                  "required": True
              },
              'test': {
                  "type": HttpUrl,
                  'required': False
              },
          }
    ```

    Above would resolve `dev` to `int` type and validate if it is greater than `4` and is not None. Similarly, it will check it `test` is not `None` and is a valid `Url`.

    Valid Validation Options:

    - `default`: since this is replacing the field’s default, its first argument is used
      to set the default, use ellipsis (`...`) to indicate the field is required
    - `alias`: the public name of the field
    - `title`: can be any string, used in the schema
    - `description`: can be any string, used in the schema
    - `gt`: only applies to numbers, requires the field to be "greater than". The schema
      will have an `exclusiveMinimum` validation keyword
    - `ge`: only applies to numbers, requires the field to be "greater than or equal to". The
      schema will have a `minimum` validation keyword
    - `lt`: only applies to numbers, requires the field to be "less than". The schema
      will have an `exclusiveMaximum` validation keyword
    - `le`: only applies to numbers, requires the field to be "less than or equal to". The
      schema will have a `maximum` validation keyword
    - `multiple_of`: only applies to numbers, requires the field to be "a multiple of". The
      schema will have a `multipleOf` validation keyword
    - `allow_inf_nan`: only applies to numbers, allows the field to be NaN or infinity (+inf or -inf),
      which is a valid Python float. Default True, set to False for compatibility with JSON.
    - `max_digits`: only applies to Decimals, requires the field to have a maximum number
      of digits within the decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
    - `decimal_places`: only applies to Decimals, requires the field to have at most a number of decimal places
      allowed. It does not include trailing decimal zeroes.
    - `min_length`: only applies to strings, requires the field to have a minimum length. The
      schema will have a `minLength` validation keyword
    - `max_length`: only applies to strings, requires the field to have a maximum length. The
      schema will have a `maxLength` validation keyword
    - `allow_mutation`: a boolean which defaults to True. When False, the field raises a TypeError if the field is
      assigned on an instance. The BaseModel Config must set validate_assignment to True
    - `regex`: only applies to strings, requires the field match against a regular expression
      pattern string. The schema will have a `pattern` validation keyword
    - `repr`: show this field in the representation

  - `eagerly_validate`: If True, the env variables will be validated on class creation, else will be validated when accessed. By default, Metaclass does not validate `env variables` of class creation for its lazy behaviour.

    > Setting this flag to True does not populate value of the elements if validation fails.

    ```python
      class Abc(BaseEnv):
        class Config(BaseConfig):
            envs = ('dev', 'test')
            validations = {
                'dev': {
                    "alias": "dev",
                    "gt": 4,
                    "type": int,
                    "required": True
                },
                'test': {
                    "type": HttpUrl,
                    'required': False
                },
            }
            eagerly_validate = True
    ```

  Above will validate all the envs on class creation and will raise and error if any mis validations found.

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
          # validations for envs
          validations = {
              'DB_PORT': {
                  "type": int,
                  "required": True
              },
              'DB_HOST': {
                  "type": str,
                  'required': True
              },
          }
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

  class ABC(metaclass=EnvMeta):
    # will create and populate env properties on ABC
    def generate_uri(self):
        return f'{self.DB_HOST}:{self.DB_PORT}'
    class Config(BaseConfig):
        envs = ('dev', ('test', 'test_value'),
                'prd', 'DB_HOST', 'DB_PORT')
        dot_env_path = Path(__file__).parent / '.env.test'
        # validations for envs
        validations = {
              'DB_PORT': {
                  "type": int,
                  "required": True
              },
              'DB_HOST': {
                  "type": str,
                  'required': True
              },
          }

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

        # validations for envs
          validations = {
              'DB_PORT': {
                  "type": int,
                  "required": True
              },
              'DB_HOST': {
                  "type": str,
                  'required': True
              },
          }

          # path to dotenv file, automatically detects .env
          # dot_env_path = pathlib.Path(__file__).parent / ".env.sample"

          # Validates of class creation if set to True
          # eagerly_validate = True

          # if True, Keeps env contained else propogates to global env
          # contained = True
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

All the Validations are done using [`Pydantic`](https://docs.pydantic.dev/) Library. Validation Errors are `Pydantic ValidationError` Instances that can be caught and JSON serialised if required.

### Contribution

---

Thank you for considering to help out with the source code! We welcome any contributions no matter how small they are!

If you'd like to contribute to `lazy_env_configurator`, please fork, fix, commit and send a pull request for the maintainers to review and merge into the main code base.

Please make sure your contributions adhere to our coding guidelines:

- Code must adhere to the official [Python Formatting](https://peps.python.org/pep-0008/) guidelines.
- Code must be documented adhering to the official Python [Documentation](https://devguide.python.org/documentation/) guidelines.
- Pull requests need to be based on and opened against the `master` branch.
- Open an issue before submitting a PR for non-breaking changes.
- Publish a VEP proposal before submitting a PR for breaking changes.

### License

---

The `lazy-env-configurator` source code is licensed under [MIT](https://opensource.org/license/mit/), also included in the `LICENSE` file.

### CHANGELOG

---

To check what changed, please refer [CHANGELOG](CHANGELOG.md).

---

Made with Love by [@satyamsoni](https://github.com/satyamsoni2211/) .

> Follow me on: [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=whitehttps://img.shields.io/twitter/follow/_satyamsoni_?style=social)](https://twitter.com/_satyamsoni_) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/-satyamsoni/) [![Github](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white)](https://github.com/satyamsoni2211)
