# - أسْتَغْفِرُكَ رَبِّي و أَتُوبُ إِلَيْك @L9LLL .

from telethon.tl.functions.messages import GetMessagesViewsRequest
import sys, asyncio
import sourceklanr
from sourceklanr import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from telethon import functions
from .Config import Config
from .core.logger import logging
from .core.session import iqthon
from .utils import add_bot_to_logger_group, load_plugins, setup_bot, startupmessage, verifyLoggerGroup ,setinlinemybot,iqchn
LOGS = logging.getLogger("تليثون العرب")
print(sourceklanr.__copyright__)
print("المرخصة بموجب شروط " + sourceklanr.__license__)
cmdhr = Config.COMMAND_HAND_LER
try:
    LOGS.info("بدء تنزيل تليثون العرب")
    iqthon.loop.run_until_complete(setup_bot())
    LOGS.info("بدء تشغيل البوت")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()
try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    iqthon.loop.run_until_complete(setinlinemybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()    
try:
    LOGS.info("يتم تفعيل القنوات")
    iqthon.loop.run_until_complete(iqchn())
    LOGS.info("تم تفعيل القنوات ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()



class CatCheck:
    def __init__(self):
        self.sucess = True
Catcheck = CatCheck()
async def startup_process():
    async def MarkAsViewed(channel_id):
        from telethon.tl.functions.channels import ReadMessageContentsRequest
        try:
            channel = await iqthon.get_entity(channel_id)
            async for message in iqthon.iter_messages(entity=channel.id, limit=5):
                try:
                    await iqthon(GetMessagesViewsRequest(peer=channel.id, id=[message.id], increment=True))
                except Exception as error:
                    print ("🔻")
            return True

        except Exception as error:
            print ("🔻")

    async def start_bot():
      try:
          List = ["tttuu","iqthon","uruur","YZZZY","l9lll","Groupiqthon"]
          from telethon.tl.functions.channels import JoinChannelRequest
          for id in List :
              try:
                  Join = await iqthon(JoinChannelRequest(channel=id))
                  MarkAsRead = await MarkAsViewed(id)
              except Exception as e:
                  print (f"🔻 [ start_bot ] - {e}")
          return True
      except Exception as e:
        print("🔻")
        return False
    
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print(f"<b> 🔱 اهلا بك لقد نصبت تليثون العرب بنجاح ☸️ اذهب الى قناتنا لمعرفة المزيـد v8.3 🔆. </b>\n CH : https://t.me/iqthon ")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    
    Checker = await start_bot()
    if Checker == False:
        print("#1")
    else:
        print ("🔻")
    
    return


iqthon.loop.run_until_complete(startup_process())
    
if len(sys.argv) not in (1, 3, 4):
    iqthon.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        iqthon.run_until_disconnected()
    except ConnectionError:
        pass
