from nonebot import on_command , on_message
from nonebot.adapters.cqhttp import MessageSegment, Message, permission, GroupMessageEvent
from nonebot.rule import keyword, startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from tools.pixiv.pixiv import a60

main = on_message(rule=startswith('牛牛涩涩'),
                priority=10,
                block=True,
                permission=permission.GROUP)

status = {}


@main.handle()
async def ma(bot: Bot, event: GroupMessageEvent, state: T_State):
    s = status.get(event.group_id)
    if s:
        p = (await a60())[0]
        url = f'https://www.pixiv.net/artworks/{p.id}'
        msg: Message = MessageSegment.text(url) + MessageSegment.image(file=p.pic)
        await main.finish(msg)
    else:
        await main.finish("听啊，悲鸣停止了。这是幸福的和平到来前的宁静。")


switch = on_message(
    rule=keyword("牛牛可以涩涩", "牛牛不可以涩涩"), 
    block=True,
    priority=5,
    permission=permission.GROUP_ADMIN | permission.GROUP_OWNER)

@switch.handle()
async def sw(bot: Bot, event: GroupMessageEvent, state: T_State):
    s = event.get_plaintext()
    if '不' in s:
        status[event.group_id] = False
        await switch.finish("再转身回头的时候，我们将带着胜利归来。")
    else:
        status[event.group_id] = True
        await switch.finish("不需畏惧，我们会战胜那些鲁莽的家伙！")
