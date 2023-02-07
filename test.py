import os
import time
from src.db import DB, Sql
from src.main import message_processor, KEYWORDS
from src.utils import get_object_values, get_now_time
import sys

user_1 = 123456789
user_2 = 987654321
user_3 = 1233
user_1_nickname = '用户1'
user_2_nickname = "'; select true; --"
group = 123

k = get_object_values(KEYWORDS)
print(k)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


snapshot = []


def wrap(user: int, message: str, at_qq: int = None, comment: str = None):
    if comment:
        print(bcolors.OKGREEN + "------" + comment + "------" + bcolors.ENDC)
        snapshot.append(comment)

    def impl_send_message(qq: int, group: int, message: str):
        print(message)
        snapshot.append(message)
    nickname = None
    if user == user_1:
        nickname = user_1_nickname
    elif user == user_2:
        nickname = user_2_nickname
    message_processor(
        message=message,
        qq=user,
        group=group,
        at_qq=at_qq,
        nickname=nickname,
        impl_send_message=impl_send_message
    )


log_arg = ''


def write_snapshot():
    global snapshot, log_arg
    timestamp = int(time.time())
    dir = f'./__snapshot__/{log_arg}'
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(f'{dir}/snapshot-{timestamp}.txt', 'w') as f:
        f.write('\n'.join(snapshot))


def clear_database():
    base_db_path = os.path.join(os.path.dirname(__file__), 'src', 'data-v2')
    if os.path.exists(base_db_path):
        print('remove old data')
        os.system(f'rm -rf {base_db_path}')


def arg(str: str):
    match = len(sys.argv) > 1 and sys.argv[1] == str
    if match:
        print(f'arg: {str}')
        global log_arg
        log_arg = f'{str}'
    return match


def test_legacy():

    wrap(user_1, '打胶', comment='没注册')
    wrap(user_1, '牛子', comment='没注册')
    wrap(user_1, '注册牛子', comment='注册')
    wrap(user_1, '打胶', user_2, comment='打胶别人失败')
    wrap(user_1, 'pk', user_2, comment='pk 别人失败')
    wrap(user_1, '🔒', user_2, comment='🔒别人失败')
    wrap(user_1, '牛子', comment='查牛子信息')

    wrap(user_2, '牛子', comment='没注册')
    wrap(user_2, '注册牛子', comment='对方注册')
    wrap(user_2, '牛子', comment='user 2 查牛子信息')
    wrap(user_2, '打胶', comment='user 2 自己打胶 l+1')
    wrap(user_2, '🔒我', comment='user 2 自己🔒自己 s+1')
    wrap(user_2, '牛子', user_1, comment='user 2 查牛子是否短了')
    wrap(user_2, 'pk', comment='None')
    wrap(user_2, '🔒', comment='None')
    wrap(user_2, '打胶', user_1, comment='user 2 打胶 user 1 l+2')
    wrap(user_2, '🔒', user_1, comment='user 2 🔒 user 1 s+2')
    wrap(user_2, 'pk', user_1, comment='user 2 pk user p+1')
    wrap(user_1, '牛子', user_1, comment='user 1 查牛子是否变了')

    # cd
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+2')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+3')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+4')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+5 cd')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+6 cd')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+3')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+4')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+5 cd')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+6 cd')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+3')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+4')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+5 cd')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+6 cd')

    wrap(user_1, '牛子', comment='user 1 查牛子是否变了')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+1')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+2')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+3')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+4')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+5 cd')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+1')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+2')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+3')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+4')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+5 cd')

    # self
    wrap(user_1, 'pk', user_1, 'user 1 pk 自己 p+1')
    wrap(user_1, '🔒', user_1, 'user 1 🔒 自己 s+6 cd')
    wrap(user_1, '打胶', user_1, 'user 1 打胶 自己 l+6 cd')

    # 查信息
    wrap(user_1, '牛子', comment='user 1 查牛子信息')
    wrap(user_2, '牛子', comment='user 2 查牛子信息')

    # 隔日
    data = DB.load_data(user_1)
    data['latest_daily_lock'] = '2020-01-01 00:00:01'
    data['pked_time'] = '2020-01-01 00:00:01'
    DB.write_data(data)
    wrap(user_1, '牛子', comment='user 1 隔日查牛子信息')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+1')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+2')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+3')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+4')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+5 cd')

    # 大额惩罚机制
    data = DB.load_data(user_1)
    data['length'] = 25
    data['latest_daily_lock'] = '2020-01-01 00:00:01'
    DB.write_data(data)
    wrap(user_1, '牛子', comment='大额惩罚机制 user 1 查牛子信息')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+1')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+2')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+3')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+4')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+5 cd')
    wrap(user_1, '🔒', user_2, comment='user 1 🔒别人 l+6 cd')

    # max
    data = DB.load_data(user_1)
    data['daily_lock_count'] = 6
    data['daily_glue_count'] = 5
    data['latest_daily_glue'] = get_now_time()
    data['daily_pk_count'] = 6
    data['latest_daily_pk'] = get_now_time()
    DB.write_data(data)
    wrap(user_1, '🔒', user_2, comment='user 1 🔒 user 2 max')
    wrap(user_1, '打胶', user_2, comment='user 1 打胶 user 2')
    wrap(user_1, '打胶', user_2, comment='user 1 打胶 user 2 max')
    wrap(user_1, 'pk', user_2, comment='user 1 pk user 2 max')

    # 看别人牛子
    wrap(user_1, '看他牛子', user_2, comment='user 1 查 user 2 牛子信息')
    wrap(user_1, '看他牛子', comment='None')

    # pk保护
    data = DB.load_data(user_1)
    data['length'] = 5
    DB.write_data(data)
    data = DB.load_data(user_2)
    data['latest_daily_pk'] = '2020-01-01 00:00:01'
    DB.write_data(data)
    wrap(user_2, 'pk', user_1, comment='user 2 pk user 1 触发 pk 保护')
    wrap(user_2, 'pk', user_1, comment='user 2 pk user 1 触发 pk 保护 +2')


def test_nickname():
    wrap(user_1, '注册牛子', comment='1 注册')
    wrap(user_2, '注册牛子', comment='2 注册')
    wrap(user_3, '注册牛子', comment='3 注册')

    # 查排名
    wrap(user_1, '牛子排名', comment='user 1 查排名')

    # 删掉 user_3 的 info 表记录，模拟增量场景
    Sql.sub_table_info.delete_single_data(user_3)

    # 改名字
    global user_1_nickname
    user_1_nickname = '用户1新名字'
    wrap(user_1, '牛子排名', comment='user 1 改名再查排名')


def test_rebirth():
    wrap(user_1, '注册牛子', comment='1 注册')
    wrap(user_2, '注册牛子', comment='2 注册')

    wrap(user_1, '牛子转生', comment='user 1 不能转生')

    data = DB.load_data(user_1)
    data['length'] = 199
    DB.write_data(data)
    wrap(user_1, '牛子转生', comment='user 1 不能转生 +1')

    data = DB.load_data(user_1)
    data['length'] = 200
    DB.write_data(data)
    wrap(user_1, '牛子转生', comment='user 1 一转')

    wrap(user_1, '牛子', comment='user 1 查个人信息')

    wrap(user_1, '牛子转生', comment='user 1 不能转生')

    data = DB.load_data(user_1)
    data['length'] = 1000
    DB.write_data(data)
    wrap(user_1, '牛子转生', comment='user 1 积攒太多再二转')
    wrap(user_1, '牛子', comment='user 1 查个人信息')
    wrap(user_1, '牛子转生', comment='user 1 三转')
    wrap(user_1, '牛子', comment='user 1 查个人信息')

    wrap(user_1, '牛子转生', comment='user 1 不能再转 +1')
    wrap(user_1, '牛子转生', comment='user 1 不能再转 +2')
    wrap(user_1, '牛子转生', comment='user 1 不能再转 +3')
    wrap(user_1, '牛子排行', comment='user 1 查排行')


if __name__ == '__main__':
    clear_database()

    # args: --legacy
    if arg('--legacy'):
        test_legacy()

    # args: --nickname
    if arg('--nickname'):
        test_nickname()

    # args: --rebirth
    if arg('--rebirth'):
        test_rebirth()

    write_snapshot()
