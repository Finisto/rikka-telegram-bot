#by Linaname
from telegram import ChatAction
from telegram.ext import CommandHandler
import requests
import random


def module_init(gd):
    commands = gd.config["commands"]
    for command in commands:
        gd.dp.add_handler(CommandHandler(command, gelbooru_search, pass_args=True))


def gelbooru_search(bot, update, args):
    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    query = " ".join(args)
    try:
        direct_link, page_link = get_image(query)
    except:
        update.message.reply_text("Sorry, something went wrong!")
        return
    if direct_link is None:
        update.message.reply_text("Nothing found!")
        return
    msg_text = "[Image]({})".format(direct_link) + "\n" + "[View post]({})".format(page_link)
    update.message.reply_text(msg_text, parse_mode="Markdown")


def get_image(query):
    params = {
        "page": "dapi",
        "s": "post",
        "q": "index",
        "json": "1",
        "tags": query,
    }
    response = requests.get("https://gelbooru.com/index.php", params=params)
    if not response.text:
        return None, None
    result_list = response.json()
    if not result_list:
        return None, None
    post = random.choice(result_list)
    direct_link, page_link = post.get("file_url"), "https://gelbooru.com/index.php?page=post&s=view&id="+str(post.get("id"))
    return direct_link, page_link
