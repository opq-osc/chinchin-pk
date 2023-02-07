from .config import Config
from .db import DB

cache = {
    'config': None
}


class RebirthSystem():

    @staticmethod
    def get_rebirth_config():
        if cache['config'] is not None:
            return cache['config']
        config = Config.get_config('rebirth')
        levels = config['levels']
        # sort by level
        levels = sorted(levels, key=lambda x: x['level'])
        # calc acc need length
        for i in range(len(levels)):
            current_level_cost_length = levels[i]['cost_length']
            if i == 0:
                levels[i]['acc_need_length'] = current_level_cost_length
            else:
                prev_level_acc_need_length = levels[i-1]['acc_need_length']
                levels[i]['acc_need_length'] = current_level_cost_length + \
                    prev_level_acc_need_length
        cache['config'] = levels
        return levels

    @staticmethod
    def calc_failed_info(level: dict):
        is_failed = Config.is_hit_with_rate(level['fail_prob'])
        failed_punish_length = 0
        if is_failed:
            failed_punish_length = Config.random_value(
                level['fail_negative_min'],
                level['fail_negative_max']
            )
        return {
            'is_failed': is_failed,
            'failed_punish_length': failed_punish_length,
        }

    @classmethod
    def get_rebirth_info(cls, qq: int):
        user = DB.load_data(qq)
        rebirth_info = DB.sub_db_rebirth.get_rebirth_data(qq)
        rebirth_config = cls.get_rebirth_config()
        if rebirth_info is None:
            first_level_info = rebirth_config[0]
            min_rebirth_length = first_level_info['acc_need_length']
            if user['length'] < min_rebirth_length:
                return {
                    'can_rebirth': False,
                }
            failed_info = cls.calc_failed_info(first_level_info)
            return {
                'can_rebirth': True,
                'current_level_info': None,
                'next_level_info': first_level_info,
                'failed_info': failed_info,
            }
        else:
            current_level = rebirth_info['level']
            max_level_info = rebirth_config[-1]
            if current_level == max_level_info['level']:
                return {
                    'can_rebirth': False,
                }
            # find current level index in array
            current_level_idx = 0
            for i in range(len(rebirth_config)):
                if rebirth_config[i]['level'] == current_level:
                    current_level_idx = i
                    break
            next_level_info = rebirth_config[current_level_idx+1]
            if user['length'] < next_level_info['acc_need_length']:
                return {
                    'can_rebirth': False,
                }
            failed_info = cls.calc_failed_info(next_level_info)
            return {
                'can_rebirth': True,
                'current_level_info': rebirth_config[current_level_idx],
                'next_level_info': next_level_info,
                'failed_info': failed_info,
            }

    @classmethod
    def get_rebirth_view_by_level(cls, level: int, length: int):
        rebirth_config = cls.get_rebirth_config()
        for level_info in rebirth_config:
            if level_info['level'] == level:
                pure_length = length - level_info['acc_need_length']
                return {
                    'current_level_info': level_info,
                    'pure_length': pure_length,
                }
        # impossible: throw exception
        raise Exception('level not found: 当你看到这个错误时，说明你的转生数据库和配置间出现了 level 匹配差错')
        