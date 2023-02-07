import os
import random
from .utils import fixed_two_decimal_digits

try:
    import ujson as json
except ImportError:
    import json

config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
cache = None


class Config():

    @staticmethod
    def read_config():
        # TODO: 检测 config.json 变化重新加载
        global cache
        if cache:
            return cache
        with open(config_file_path, 'r') as f:
            cache = json.load(f)
            return cache

    @staticmethod
    def modify_config_in_runtime(key: str, value):
        """
          for test only
        """
        global cache
        cache[key] = value

    @classmethod
    def get_config(cls, key: str):
        config = cls.read_config()
        return config.get(key)

    @classmethod
    def new_chinchin_length(cls):
        min = cls.get_config('new_chinchin_length_random_min')
        max = cls.get_config('new_chinchin_length_random_max')
        return cls.random_value(min, max)
    
    @staticmethod
    def random_value(min: float, max: float):
        return fixed_two_decimal_digits(
            min + (max - min) * random.random(),
            to_number=True
        )

    @staticmethod
    def is_hit_with_rate(rate: float):
        return random.random() < rate

    @classmethod
    def is_hit(cls, key: str):
        rate = cls.get_config(key)
        return cls.is_hit_with_rate(rate)

    @classmethod
    def get_lock_me_punish_value(cls):
        min = cls.get_config('lock_me_negative_min')
        max = cls.get_config('lock_me_negative_max')
        return cls.random_value(min, max)

    @classmethod
    def get_lock_plus_value(cls):
        min = cls.get_config('lock_plus_min')
        max = cls.get_config('lock_plus_max')
        return cls.random_value(min, max)

    @classmethod
    def get_glue_plus_value(cls):
        min = cls.get_config('glue_plus_min')
        max = cls.get_config('glue_plus_max')
        return cls.random_value(min, max)

    @staticmethod
    def is_pk_win():
        return random.random() < 0.5

    @classmethod
    def get_pk_plus_value(cls):
        min = cls.get_config('pk_plus_min')
        max = cls.get_config('pk_plus_max')
        return cls.random_value(min, max)

    @classmethod
    def get_pk_punish_value(cls):
        min = cls.get_config('pk_negative_min')
        max = cls.get_config('pk_negative_max')
        return cls.random_value(min, max)

    @classmethod
    def get_glue_punish_value(cls):
        min = cls.get_config('glue_negative_min')
        max = cls.get_config('glue_negative_max')
        return cls.random_value(min, max)

    @classmethod
    def get_lock_punish_with_strong_person_value(cls):
        min = cls.get_config('lock_me_negative_with_strong_person_min')
        max = cls.get_config('lock_me_negative_with_strong_person_max')
        return cls.random_value(min, max)

    @classmethod
    def get_glue_self_punish_value(cls):
        min = cls.get_config('glue_self_negative_min')
        max = cls.get_config('glue_self_negative_max')
        return cls.random_value(min, max)
