#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.utils import caption_filter, get_image, send_image, get_param
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.dispatcher import run_async
from telegram import ChatAction
import subprocess
import datetime
import legofy


def module_init(gd):
    global path, extensions
    path = gd.config["path"]
    extensions = gd.config["extensions"]
    commands = gd.config["commands"]
    for command in commands:
        gd.dp.add_handler(MessageHandler(caption_filter("/"+command), lego))
        gd.dp.add_handler(CommandHandler(command, lego))


@run_async
def lego(bot, update):
    filename = datetime.datetime.now().strftime("%d%m%y-%H%M%S%f")
    size = get_param(update)
    try:
        extension = get_image(bot, update, path, filename)
    except:
        update.message.reply_text("Can't get the image! :(")
        return
    if extension not in extensions:
        update.message.reply_text("Unsupported file, onii-chan!")
        return False
    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    if extension == ".webp" or ".png":
        stick = "convert " + path + filename + extension + " -background white -flatten " + path + "original" + extension
        subprocess.run(stick, shell=True)
    legofy.main(image_path=path + filename + extension,
                output_path=path + filename + "-lego" + extension,
                size=size, palette_mode=None, dither=False)
    send_image(update, path, filename+"-lego", extension)
    print(datetime.datetime.now(), ">>>", "lego", ">>>", update.message.from_user.username)
