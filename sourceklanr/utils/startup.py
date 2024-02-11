import asyncio
import glob
import os
import sys
import requests
from asyncio.exceptions import CancelledError
from datetime import timedelta
from pathlib import Path
from telethon import Button, functions, types, utils
from sourceklanr import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from telethon.tl.functions.channels import JoinChannelRequest
from ..core.logger import logging
from ..core.session import iqthon
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import del_keyword_collectionlist, get_item_collectionlist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .klanr import load_module
from .tools import create_supergroup
LOGS = logging.getLogger("تليثون العرب \n ")
cmdhr = Config.COMMAND_HAND_LER
TG_BOT = Config.TG_BOT_USERNAME
async def load_plugins(folder):
    path = f"sourceklanr/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(shortname.replace(".py", ""),  plugin_path=f"sourceklanr/{folder}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"sourceklanr/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"sourceklanr/{folder}/{shortname}.py"))
                LOGS.info(f"⁂ ︙غير قادر على التحميل {shortname} يوجد هناك خطا بسبب : {e}"                )
async def startupmessage():
    try:
        if BOTLOG:
            Config.CATUBLOGO = await iqthon.tgbot.send_file(BOTLOG_CHATID, "https://telegra.ph/file/388e81c2cdc1664ccb652.jpg", caption="**⁂ - تـمّ  اعـادة تشـغيل .\n⁂ - تليثـون العـرب ( 8.3 ) .\n\n⁂ - اوامر السورس : ( .الاوامر  ) \n\n⁂ - لمـعرفة كيفية تغير بعض كلايش او صور السـورس  أرسـل  : (  .مساعده  )\n\n⁂ - القناة تليثون العرب : @IQTHON \n\n❕- يتم اعادة التشغيل كل 24 ساعة ⁂**",                buttons=[(Button.url("مطور تليثون الرسمي", "https://t.me/GGGKG"),)],            )
    except Exception as e:
        LOGS.error(e)
        return None

async def setinlinemybot():
    try:
        inlinestarbot = await iqthon.tgbot.get_me()
        bot_name = inlinestarbot.first_name
        botname = f"@{inlinestarbot.username}"
        Arab = "IQTHON ARAB"
        if bot_name.endswith("Assistant"):
            print("تم تشغيل البوت")
        if inlinestarbot.bot_inline_placeholder:
            print("Arab 🟢")
        else:
            try:
                await iqthon.send_message("@BotFather", "/setinline")
                await iqthon.JoinChannelRequest('@Groupiqthon')
                await asyncio.sleep(1)
                await iqthon.send_message("@BotFather", botname)
                await asyncio.sleep(1)
                await iqthon.send_message("@BotFather", Arab)
                await asyncio.sleep(2)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

async def add_bot_to_logger_group(chat_id):
    bot_details = await iqthon.tgbot.get_me()
    try:
        await iqthon(            functions.messages.AddChatUserRequest(                chat_id=chat_id,                user_id=bot_details.username,                fwd_limit=1000000            )        )
    except BaseException:
        try:
            await iqthon(
                functions.channels.InviteToChannelRequest(                    channel=chat_id,                    users=[bot_details.username]                )            )
        except Exception as e:
            LOGS.error(str(e))
async def setup_bot():
    try:
        await iqthon.connect()
        config = await iqthon(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == iqthon.session.server_address:
                if iqthon.session.dc_id != option.id:
                    LOGS.warning(                        f"⁂ ︙ معرف DC ثابت في الجلسة من {iqthon.session.dc_id}"                        f"⁂ ︙ يتبع ل {option.id}"                    )
                iqthon.session.set_dc(option.id, option.ip_address, option.port)
                iqthon.session.save()
                break
        bot_details = await iqthon.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await iqthon.start(bot_token=Config.TG_BOT_USERNAME)
        iqthon.me = await iqthon.get_me()
        iqthon.uid = iqthon.tgbot.uid = utils.get_peer_id(iqthon.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(iqthon.me)
    except Exception as e:
        LOGS.error(f"قم بتغير كود تيرمكس - {str(e)}")
        sys.exit()

async def iqchn():
    try:
        os.environ[            "STRING_SESSION"        ] = "**⎙ :: انتبه عزيزي المستخدم هذا الملف ملغم يمكنه اختراق حسابك لم يتم تنصيبه في حسابك لا تقلق.**"
    except Exception as e:
        print(str(e))
    try:

        await iqthon(JoinChannelRequest("@m8m8m"))
    except BaseException:
        pass

async def verifyLoggerGroup():
    flag = False
    if BOTLOG:
        try:
            entity = await iqthon.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "⁂ ︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "⁂ ︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."                    )
        except ValueError:
            LOGS.error("⁂ ︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(                "⁂ ︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."            )
        except Exception as e:
            LOGS.error(                "⁂ ︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"                + str(e)            )
    else:
        descript = "⁂ ︙ لا تحذف هذه المجموعة أو تغير إلى مجموعة (إذا قمت بتغيير المجموعة ، فسيتم فقد كل شيئ .)"
        iqphoto1 = await iqthon.upload_file(file="SQL/extras/iqthon1.jpg")
        _, groupid = await create_supergroup(            "تخزين تليثون العرب العام", iqthon, Config.TG_BOT_USERNAME, descript  ,  iqphoto1 )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("⁂ ︙ تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await iqthon.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "⁂ ︙ الأذونات مفقودة لإرسال رسائل لـ PM_LOGGER_GROUP_ID المحدد."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "⁂ ︙الأذونات مفقودة للمستخدمين الإضافيين لـ PM_LOGGER_GROUP_ID المحدد."                    )
        except ValueError:
            LOGS.error("⁂ ︙ لا يمكن العثور على فار  PM_LOGGER_GROUP_ID. تأكد من صحتها.")
        except TypeError:
            LOGS.error("⁂ ︙ PM_LOGGER_GROUP_ID غير مدعوم. تأكد من صحتها.")
        except Exception as e:
            LOGS.error(                "⁂ ︙ حدث استثناء عند محاولة التحقق من PM_LOGGER_GROUP_ID.\n" + str(e)            )
    else:
        descript = "⁂ ︙ وظيفه هذا المجموعة لحفض رسائل التي تكون موجة اليك ان لم تعجبك هذا المجموعة قم بحذفها نهائيأ 👍 \n  الـسورس : - @IQTHON"
        iqphoto2 = await iqthon.upload_file(file="SQL/extras/iqthon2.jpg")
        _, groupid = await create_supergroup(            "تخزين تليثون العرب الخاص", iqthon, Config.TG_BOT_USERNAME, descript    , iqphoto2  )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("⁂ ︙ تم إنشاء مجموعة خاصة لـ PRIVATE_GROUP_BOT_API_ID بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "sourceklanr"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
