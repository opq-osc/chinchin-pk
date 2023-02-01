from botoy import GroupMsg, S
from botoy import async_decorators as deco
from botoy import jconfig, logger
from botoy.collection import MsgTypes
from botoy.parser import group as gp

from .src.main import message_processor, KEYWORDS
from .src.utils import get_object_values, create_match_func_factory

__version__ = "2.2.2"
__doc__ = f"""牛子系统 v{__version__}
可用的指令/功能有：
""" + "、".join(
    [
        "/".join(KEYWORDS.get("chinchin")),
        "/".join([i + "@某人" for i in KEYWORDS.get("pk")]),
        "/".join(KEYWORDS.get("lock_me")),
        "/".join([i + "@某人" for i in KEYWORDS.get("lock")]),
        "/".join(KEYWORDS.get("glue")),
        "/".join([i + "@某人" for i in KEYWORDS.get("see_chinchin")]),
        "/".join(KEYWORDS.get("sign_up")),
        "/".join(KEYWORDS.get("ranking")),
    ]
)
config = jconfig.get_configuration("chinchin_system")
groups = config.get("groups")

logger.info(f"{__doc__}:监听群组:{groups}")

keywords = get_object_values(KEYWORDS)
match_func = create_match_func_factory(fuzzy=True)

@deco.ignore_botself
@deco.from_these_groups(*groups)
@deco.these_msgtypes(MsgTypes.TextMsg, MsgTypes.AtMsg)
async def receive_group_msg(ctx: GroupMsg):
    from_user = ctx.FromUserId
    group = ctx.FromGroupId
    nickname = ctx.FromNickName

    def impl_at_segment(qq: int):
        return ctx.FromNickName

    def impl_send_message(qq: int, group: int, message: str):
        S.bind(ctx).text(message)
        return

    if ctx.MsgType == MsgTypes.AtMsg:
        at_data = gp.at(ctx)
        # FIXME: at all 时 at_data 为 None
        if not at_data:
            return
        # 只对 at 一个人生效
        if len(at_data.UserExt) != 1:
            return
        content = at_data.Content.strip()
        if not match_func(keywords=keywords, text=content):
            return
        target = at_data.UserExt[0].QQUid
        message_processor(
            message=content,
            qq=from_user,
            at_qq=target,
            group=group,
            fuzzy_match=True,
            nickname=nickname,
            impl_at_segment=impl_at_segment,
            impl_send_message=impl_send_message
        )
        return
    elif ctx.MsgType == MsgTypes.TextMsg:
        content = ctx.Content
        if not match_func(keywords=keywords, text=content):
            return
        message_processor(
            message=content,
            qq=from_user,
            group=group,
            fuzzy_match=True,
            nickname=nickname,
            impl_at_segment=impl_at_segment,
            impl_send_message=impl_send_message
        )
        return
