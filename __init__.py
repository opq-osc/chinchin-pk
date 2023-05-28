from botoy import  S,ctx,mark_recv
from botoy import jconfig, logger


from .src.main import message_processor, KEYWORDS, VERSION, HELPPER
from .src.utils import get_object_values, create_match_func_factory

# __version__ = VERSION
# __doc__ = HELPPER
# config = jconfig.get_configuration("chinchin_system")
# groups = config.get("groups")
#
# logger.info(f"{__doc__}:监听群组:{groups}")

keywords = get_object_values(KEYWORDS)
match_func = create_match_func_factory(fuzzy=True)


async def chichipk():
    if g:= ctx.g:
        from_user = g.from_user
        group = g.from_group
        nickname = g.from_user_name
        print(g.images)

        def impl_at_segment(qq: int):
            # 伪 at ，因为真 at 会风控
            return f'@{g.from_user_name}'

        async def impl_send_message(qq: int, group: int, message: str):
            await S.text(message)
            return

        if g.at_list != [] :
            data = len(g.from_user_name)+2
            at_data = g.text[data:]
            # FIXME: at all 时 at_data 为 None
            if not at_data:
                return
            # 只对 at 一个人生效
            if len(g.at_list) != 1:
                return
            content = at_data
            if not match_func(keywords=keywords, text=content):
                return
            target = g.at_list[0].Uin
            await message_processor(
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
        elif g.images == None:
            content = g.text
            if not match_func(keywords=keywords, text=content):
                return
            await message_processor(
                message=content,
                qq=from_user,
                group=group,
                fuzzy_match=True,
                nickname=nickname,
                impl_at_segment=impl_at_segment,
                impl_send_message=impl_send_message
            )
            return
mark_recv(chichipk)