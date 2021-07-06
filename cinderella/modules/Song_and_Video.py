#code by nousername_psycho
from cinderella import pbot as app
from pyrogram import filters
import youtube_dl
from youtube_search import YoutubeSearch
import requests
import time
import os

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@app.on_message(filters.command('song'))
def pyro_song(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    m = message.reply('🔎 let me find your song.')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            duration = results[0]["duration"]
            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return
            
            
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            views = results[0]["views"]
            
#             thumb_name = f'thumb{message.message_id}.jpg'
#             thumb = requests.get(thumbnail, allow_redirects=True)
#             open(thumb_name, 'wb').write(thumb.content)
            
            

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("⏬ Downloading.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        cap = f'☈ Title : {title[:35]}\n☈ Duration: `{duration}`\n☈ Link: `[{link}](Click here)`\n\n@Misstezza_bot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=cap, parse_mode='md',quote=False, title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('❌ Error')
        print(e)
    try:
        os.remove(audio_file)    
    except Exception:
        print("error")
    
#video
@app.on_message(filters.command('video'))
def pyro_video(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    m = message.reply('🔎 let me find your video.')

    ydl_opts = {
            'format' : 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'extract-audio' : True,}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            duration = results[0]["duration"]
            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return
            
            
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            views = results[0]["views"]
            
#             thumb_name = f'thumb{message.message_id}.jpg'
#             thumb = requests.get(thumbnail, allow_redirects=True)
#             open(thumb_name, 'wb').write(thumb.content)
            
            

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
            caption = f"{title}"

       # if time_to_seconds(duration) >= 120:  # duration limit
           #  message.reply(f"⚠️ **Nooo..! its more than 2 minutes long, so i can't send it**\n\n  **No problem** 👇🏻 \n\nTry this `/video full screen status` or youtubelink id ")  
             
           #  message.reply_sticker("CAACAgEAAxkBAAIp-mA6wRwpVBHG0tX3JNvdE4c4iMnVAAJOAgACUSkNOQhvgycKvc6HHgQ") 
            # return
            m.edit("⏫ Uploading ")
            message.reply_video(video=video, caption=caption)
            
            m.delete()
            
            os.remove(video)


__help__ = """		  
 /song <songname artist(optional)>: uploads the song in it's best quality available
 /video <songname artist(optional)>: uploads the video song in it's best quality available
"""

__mod_name__ = "MUSIC"
