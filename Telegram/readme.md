# telegram bot

Telebot is a Python library for building Telegram bots. It offers various methods and handlers to interact with the Telegram Bot API. Here's an overview of the most commonly used methods and handlers with examples:

### Initialization
```python
import telebot

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
BOT_API = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(BOT_API)
```

### Streaming Message Handlers
```python
@bot.message_handler(commands=['send_text'])
def handle_message2(message):
    
    data = 'let say this is the example for streaming response'
    sent_message = bot.send_message(message.chat.id, "...")
    text=''
    for item in data.split(" "):
        if item!='':
            text += f"{item} "
            bot.edit_message_text(text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
```

#### Command Handlers
These handlers respond to specific commands.
```python
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot!")
```

#### Text Message Handler
Handles regular text messages.
```python
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
```

#### Document Handler
Handles document uploads.
```python
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_document", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Document received and saved.")
```

#### Photo Handler
Handles photo uploads.
```python
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_photo.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Photo received and saved.")
```

#### Video Handler
Handles video uploads.
```python
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_video.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Video received and saved.")
```

#### Audio Handler
Handles audio uploads.
```python
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_audio.mp3", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Audio received and saved.")
```

#### Sticker Handler
Handles sticker messages.
```python
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.reply_to(message, "Nice sticker!")
```

### Bot Methods

chat_id = message.chat.id
#### `send_message`
Sends a text message.
```python
chat_id = message.chat.id
bot.send_message(chat_id, "Hello, World!")
```
Done

#### `send_photo`
Sends a photo.
```python
chat_id = message.chat.id
bot.send_photo(chat_id, photo=open('path_to_photo.jpg', 'rb'))
```

#### `send_document`
Sends a document.
```python
bot.send_document(chat_id, document=open('path_to_document.pdf', 'rb'))
```

#### `send_audio`
Sends an audio file.
```python
bot.send_audio(chat_id, audio=open('path_to_audio.mp3', 'rb'))
```

#### `send_video`
Sends a video.
```python
bot.send_video(chat_id, video=open('path_to_video.mp4', 'rb'))
```

#### `send_sticker`
Sends a sticker.
```python
bot.send_sticker(chat_id, sticker=open('path_to_sticker.webp', 'rb'))
```

#### `send_location`
Sends a location.
```python
bot.send_location(chat_id, latitude=51.5074, longitude=-0.1278)
```



#### `send_chat_action`
Shows a typing indicator or other chat actions.
```python
bot.send_chat_action(chat_id, action='typing')
```
all  actions :
'upload_photo': Uploading a photo
'record_video': Recording a video
'upload_video': Uploading a video
'record_audio': Recording audio
'upload_audio': Uploading audio
'upload_document': Uploading a document
'find_location': Finding a location
'record_video_note': Recording a video note
'upload_video_note': Uploading a video note

### Additional Methods

#### `get_me`
Returns basic information about the bot.
```python
bot_info = bot.get_me()
print(bot_info)
```

#### `get_updates`
Returns incoming updates using long polling.
```python
updates = bot.get_updates()
```

#### `get_file`
Gets basic info about a file and prepares it for downloading.
```python
file_info = bot.get_file(file_id)
```

#### `download_file`
Downloads a file by its file path.
```python
downloaded_file = bot.download_file(file_info.file_path)
```

#### `set_webhook`
Sets a webhook URL for the bot.
```python
bot.set_webhook(url='https://example.com/webhook')
```

#### `delete_webhook`
Deletes the webhook integration.
```python
bot.delete_webhook()
```

### Example Workflow

1. **Initialization**:
   - Set up the bot with the token.
   - Define handlers for different types of messages (commands, text, files).

2. **Handling Messages**:
   - Use command handlers to respond to specific commands like `/start`.
   - Use content type handlers to manage file uploads and media.
   - Use a general text handler to manage text messages.

3. **Bot Actions**:
   - Respond to users with text, images, documents, etc.
   - Show typing indicators or other actions while processing.

4. **Deployment**:
   - Set up webhook or long polling for receiving updates.
   - Ensure the bot is running and listening for incoming messages.

This overview covers the primary methods and handlers you would use with Telebot to create a comprehensive Telegram bot. Each example provides a foundation you can expand upon based on your specific needs.
