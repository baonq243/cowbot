#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auth: BaoNQ
# Purpose: Check from core network
# - ping
# - dns
# - scan port
# - check port
# - tracert
# - mtr
# - special command

# Version: 0.1
# - Reflector code
# - Run on docker

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import os
import sys
import subprocess
import validators
import logging
from logging.handlers import RotatingFileHandler


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def bash(string):
    try:
        output = subprocess.run(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=120)
        return output.stdout
    except Exception as E:
        print(E)


def start(update, context):
    update.message.reply_markdown("\nXin chào {} !\n".format(update.message.from_user.first_name))


def help(update, context):
    update.message.reply_markdown("```\nMy CowBot\n"
                                  "/ping <ip> or <domain>\n"
                                  "/dns <domain>\n"
                                  "/scanport <ip>\n"
                                  "/checkport <ip> <port>\n"
                                  "/tracert <ip> or <domain>\n"
                                  "/mtr <ip> or <domain>\n"
                                  "/getid\n"
                                  "/checkwan <domain> <ipwan>\n"
                                  "/command command" + '```')


def getid(update, context):
    update.message.reply_markdown(
        "\nUser: {} Id: {}\n".format(update.message.from_user.first_name, update.message.from_user.id))
    update.message.reply_markdown(
        "\nId: {}\n".format(update.message.chat_id))


def command(update, context):
    if update.message.chat_id not in group_id or update.message.from_user.id not in list_admin:
        update.message.reply_markdown("```\nYou don't have permission!\n"
                                      "Liên hệ @baonq !" + '```')
    else:
        try:
            if context.args:
                command = " ".join(str(x) for x in context.args)
                result = bash(command)
                print(result)
                update.message.reply_markdown("```\n{}\n".format(result) + '```')
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n```")


def traceroute(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 1:
                    raise Exception()
                if validators.ipv4(context.args[0]) or validators.domain(context.args[0]):
                    result = bash('traceroute -n -m 30 ' + context.args[0])
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /traceroute <ip> or <domain>" + '```')


def checkwan(update, context):
    update.message.reply_markdown("```\nĐang dev bạn ôi!\n" + '```')


def dns(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 1:
                    raise Exception()
                if validators.domain(context.args[0]):
                    result = bash('nslookup ' + context.args[0])
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /dns <domain>" + '```')


def checkport(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 2:
                    raise Exception()
                if int(context.args[1]) < 1 or int(context.args[1]) > 65535:
                    update.message.reply_markdown("```\nPort range: 1 - 65535\n" + '```')
                elif validators.ipv4(context.args[0]):
                    result = bash('nmap -sTU -p {} {}'.format(context.args[1], context.args[0]))
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /checkport <ip> <port>" + '```')


def scanport(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 1:
                    raise Exception()
                if validators.ipv4(context.args[0]):
                    result = bash('nmap -n -PN -sT -sU -F {}'.format(context.args[0]))
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /scanport <ip>" + '```')


def mtr(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 1:
                    raise Exception()
                if validators.ipv4(context.args[0]) or validators.domain(context.args[0]):
                    result = bash('mtr -b -c 10 -r ' + context.args[0])
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /mtr <ip> or <domain>" + '```')


def ping(update, context):
    if update.message.chat_id not in group_id:
        update.message.reply_markdown("```\nYou don't have permission!\n" + '```')
    else:
        try:
            if context.args:
                if len(context.args) != 1:
                    raise Exception()
                if validators.ipv4(context.args[0]) or validators.domain(context.args[0]):
                    result = bash('ping -c 5 ' + context.args[0])
                    update.message.reply_markdown("```\n{}\n".format(result) + '```')
                else:
                    raise Exception()
            else:
                raise Exception()
        except Exception as error:
            print(error)
            update.message.reply_markdown("```\nLệnh không hợp lệ\n"
                                          "- /ping <ip> or <domain>" + '```')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mtr', mtr))
    dp.add_handler(CommandHandler('dns', dns))
    dp.add_handler(CommandHandler('traceroute', traceroute))
    dp.add_handler(CommandHandler('getid', getid))
    dp.add_handler(CommandHandler('checkport', checkport))
    dp.add_handler(CommandHandler('scanport', scanport))
    dp.add_handler(CommandHandler('checkwan', checkwan))
    dp.add_handler(CommandHandler('command', command))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(filename="running.log", level=logging.INFO,
                        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    logger = logging.getLogger('my_bot')
    handler = RotatingFileHandler('running.log', maxBytes=500000, backupCount=5)
    logger.addHandler(handler)

    LIST_ALLOW = os.getenv('LIST_ALLOW')
    TOKEN = os.getenv('TOKEN')
    LIST_ADMIN = os.getenv('LIST_ADMIN')
    group_id = list(map(int, str(LIST_ALLOW).split(',')))
    list_admin = list(map(int, str(LIST_ADMIN).split(',')))
    main()
