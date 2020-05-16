import time
import json
import random
import datetime
import platform
import faceRecognition

import telebot
from telebot.types import Message, InputMediaPhoto

with open('config.json') as config_file:
    config = json.load(config_file)

with open(config['paths']['commands']) as commands_file:
    commands = json.load(commands_file)

TOKEN = config['telegram']['token']
bot = telebot.TeleBot(TOKEN)
telebot.apihelper.proxy = { 'https': config['telegram']['proxy'] }

# TODO : Save and read this from db or file
admins = []
mode = 0

@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    print('Start handler')
    bot.send_message(message.chat.id, 'Mommy mod bot here! Created by @moulin666')


@bot.message_handler(commands=['help'])
def help_handler(message: Message):
    print('Help handler')
    help_text = "I am a bot using newfangled neural networks with which I can interact with you. \n\nYou can control me by sending these commands: \n\n"
    for key in commands:
        help_text += """/[{}] - {}\n""".format(key, commands[key])
        
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['ping'])
def say_hi_handler(message: Message):
    print('Ping handler')
    bot.send_video(message.chat.id, config['telegram']['startGif'], reply_to_message_id=message.message_id)


@bot.message_handler(commands=['face_mode_on'])
def face_mode_handler(message: Message):
    print('Set mode to FACE RECOGNITION')
    global mode
    mode = 0
    bot.send_message(message.chat.id, 'Set mode to *FACE RECOGNITION*', parse_mode="Markdown")


@bot.message_handler(commands=['test_mode_on'])
def test_mode_handler(message: Message):
    print('Set mode to TEST')
    global mode
    mode = 1
    bot.send_message(message.chat.id, 'Set mode to *TEST*', parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def photo_handler(message: Message):
    print('We have a photo ', message.photo)
    
    fileId = message.photo[-1].file_id
    fileInfo = bot.get_file(fileId)
    dFile = bot.download_file(fileInfo.file_path)
    with open("data/downloaded/userImg_{}.jpg".format(datetime.datetime.now().isoformat()), 'wb') as image:
        image.write(dFile)

    global mode
    if mode == 0:
        faces = faceRecognition.GetFaces(image.name)
        photos = []
        for face in faces:
            photo = open(face.name, 'rb')
            photos.append(photo)

        if len(photos) > 6:
            bot.send_message(message.chat.id, 'Too much faces on a photo. Sending first 9....')

        wordArray = ["1", "2", "3", "4", "5"]

        if len(photos) > 1:
            media = []
            i = 0
            for photo in photos:
                if i < 9:
                    random.shuffle(wordArray)
                    media.append(InputMediaPhoto(photo, '{} {}'.format(i, wordArray[0])))

                i = i + 1
                
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_media_group(message.chat.id, media, reply_to_message_id=message.message_id)
        
        if len(photos) == 1:
            random.shuffle(wordArray)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, photos[0], wordArray[0], reply_to_message_id=message.message_id)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(3)
        bot.send_message(message.chat.id, "Test mode enabled now", reply_to_message_id=message.message_id)


if __name__ == '__main__':
    while True:
        try:
            print ('Bot setup')
            bot.polling(timeout=20, none_stop=False)
        except Exception as ex:
            print ('Bot threw an exception:')
            print (str(ex))
        finally:
            print ('Bot has stopping')
            break
