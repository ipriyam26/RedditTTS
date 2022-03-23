#!venv/bin/python 
from glob import glob
from time import time
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pyttsx3
import os
import praw
from datetime import datetime
import random
import env
import sel

class Image_Processor:
    
    def __init__(self):
        pass
    
    #Function to make title png & audio
    def make_title(self,image,title,user_name,time,comments):
        
        make_title_audio(title)
        self.add_title(image=image,title=title,user_name=user_name,time=time,comments=comments)
        # return image
    
    def add_title(self,image,title,user_name,time,comments):
        ttf = glob("*.ttf")
        wrapper = textwrap.TextWrapper(width=55)
        word_list = wrapper.wrap(text=title)
        title="\n".join(word_list)
        posted = f"Posted by u/{user_name} {time}"
        image = self.add_text(image=image,text=posted,color=(157,157,163),font=ttf[1],position=(20,690),size=27)
        obj = self.add_multiline_text(image,title,(225,225,225),font=ttf[1],position=(20,750))
        image = obj[0]
        height = obj[2]
        image = self.add_image(image,Image.open("coment2.png"),position=(20,750+height+40))
        comments = f"{comments} Comments    •••"
        image = self.add_text(image,comments,(157,157,163),font=ttf[1],position=(110,750+height+50),size=27)
        image.save("test0.png")
        
        # return image
    
    #Function to make text to speech using pyttsx3 

    # Function to draw a line in an image
    def draw_line(self,image, height):
        draw = ImageDraw.Draw(image)
        draw.line((65, 390, 65, 390+height),width=3, fill=(157,157,163))
        return image 
    
    # Function to add text to an image
    def add_text(self,image, text, color,font,position,size):
        draw = ImageDraw.Draw(image)
        ff = ImageFont.truetype(font, size=size)
        draw.text(position, text, fill=color,font=ff)
        return image
    
    def add_text_base_image(self,image, text, color,font,position,size):
        draw = ImageDraw.Draw(image)
        ff = ImageFont.truetype(font, size=size)
        draw.text(position, text, fill=color,font=ff)
        font_width,font_height = draw.textsize(text, font=ff)
        return (image,font_width,font_height)
        
    # Function to add multiline text to an image
    def add_multiline_text(self,image, text, color,font,position):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, size=35)
        draw.text(position, text, fill=color, font=font)
        # draw.multiline_textbbox(position, text, font=font)
        font_width,font_height = draw.textsize(text, font=font)
        return (image,font_width,font_height)


    # Function to add an image to an image
    def add_image(self,image, image2,position=(30,285)):
        image.paste(image2, position)
        return image
    
    def resize_profile(self,image):
        width,height = image.size
        image = image.resize((int(width/3)-10,int(height/3)-10))
        return image
    
    # Function to make base image
    def base_image(self,image,profile_picture,profile_name,time):
        profile_name=f"u/{profile_name}"
        ttf = glob("*.ttf") 
        image = self.add_image(image,profile_picture)
        obj = self.add_text_base_image(image,profile_name,(0,255,255),font=ttf[1],size=32,position=(130,300))
        image = obj[0]
        time = f" • {time}"
        image = self.add_text(image,time,(157,157,163),font=ttf[1],position=(130+obj[1]+15,305),size=30)
        image = self.draw_line(image,175)
        return image
    
    # Add text now to the image
    def adding_text_line_by_line(self,image,text,likes,comment):
        ttf = glob("*.ttf")[1]
        split = text.split(".")
        if(split[-1]==""):
            split.pop(-1)
        i=0
        sen =""
        pan = []
        wrapper = textwrap.TextWrapper(width=50)
        while (i<len(split)):
            
            # if i==len(split):
            #     image = self.add_image()
            word_list = wrapper.wrap(text=f'{split[i].strip()}.')
            pan.append(word_list)
            ss = "\n".join(word_list)
            sen = sen + "\n"+ ss
            obj = self.add_multiline_text(image,sen,(225,225,225),font=ttf,position=(110,340))
            image = obj[0]
            image = self.draw_line(image,obj[2])
            if i==len(split)-1:
                image = self.add_image(image,Image.open("end.png"),position=(80,340+obj[2]+20))
                image = self.add_text(image,f"{likes}",(157,157,163),font=ttf,position=(195,340+obj[2]+50),size=30)
                image = self.add_text(image,f"{comment}",(157,157,163),font=ttf,position=(520,340+obj[2]+50),size=30)
            image.save(f"test{i+1}.png")
            # image.show()
            i+=1
        return pan    
            




def make_title_audio(title):
    title = str(title)
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')[7]
    engine.setProperty('voice', voice.id)
    engine.save_to_file(title, "test0.mp3")
    engine.runAndWait()
            
# Function to convert text to speech using google text to speech
def text_to_speech(texts):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')[7]
    engine.setProperty('voice', voice.id)
    for i, text in enumerate(texts, start=1):
        engine.save_to_file(text, f"test{i}.mp3")
    engine.runAndWait()
    
    

# Function to join image to audio using ffmpeg
def make_video(name:str):

    audios = glob("test*.mp3")
    images = glob("test*.png")
    j = random.randint(0,10)
    i=0
    while i<len(audios):
        # os.system(f"echo 'file test{i}.mp3' >> audio.txt")
        # os.system(f"echo 'file test{i}.png' >> image.txt")
        os.system(f"ffmpeg -hide_banner -loglevel error -i test{i}.png -i test{i}.mp3 -c:a aac -vcodec libx264 test{i}.mp4")
        i += 1
    videos = glob("test*.mp4")
    i=0
    videos.sort()
    while i<len(videos):
        os.system(f"echo 'file test{i}.mp4' >> list.txt")
        i += 1

    os.system(f"ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i list.txt -c copy videos/{name}.mp4")

    # os.system(f"rm list.txt && rm audio.txt && rm image.txt")
    
    os.system("rm list.txt")
    for image in glob("test*.png"):
        os.system(f"rm {image}")
    for audio in glob("test*.mp3"):
        os.system(f"rm {audio}")
    for vid in glob("test*.mp4"):
        os.system(f"rm {vid}")


    # Function to get the title of the post

   


# Function to convert time to maximum unit of time possible
def time(time):
    if(time>31557600):
        return f"{int(time/31557600)} years ago"
    elif(time>2629800):
        return f"{int(time/2629800)} months ago"
    elif(time>86400):
        return f"{int(time/86400)} days ago"
    elif(time>3600):
        return f"{int(time/3600)} hours ago"
    elif(time>60):
        return f"{int(time/60)} minutes ago"
    else:
        return f"{int(time)} seconds ago"


#API CALLS
reddit = praw.Reddit(client_id=env.CLIENT_ID,
                     client_secret=env.CLIENT_SECRET,
                     user_agent=env.USER_AGENT,
                     username=env.USERNAME,
                     password=env.PASSWORD)

subreddit = reddit.subreddit('AskReddit')
# subreddit.top(limit=10)
submissions = subreddit.hot(limit=100)
s=60
k=0
subIds=[submission.id for submission in submissions]
os.system("rm -rf videos")
os.system("mkdir videos")
total_videos = []
while k<s:
    comments=[]
    p=1
    f=0
    for subID in subIds:
        submission = reddit.submission(id=subID)

        top_comments = list(submission.comments)
        for top_comment in top_comments:

            try:
                if(len(top_comment.body)>600 and len(top_comment.body)<900):
                    f=1
                    comment = {
                        "Body": top_comment.body,
                        "comment_Author": top_comment.author.name,
                        "sub_Author": submission.author.name,
                        "sub_title": submission.title,
                        "sub_time": submission.created_utc,
                        "sub_comments": submission.num_comments,
                        "comment_likes": top_comment.score,
                        "comment_time": top_comment.created_utc,
                    }
                    comments.append(comment)

            except: 
                p+=1

        subIds = subIds[p:]        

        if(f==1):
            break   

    j=0
    while j<len(comments):
       
        #time block
        current_time = datetime.now().timestamp()
        submission_time = float(comments[j]["sub_time"])
        comment_time = float(comments[j]["comment_time"])
        sub_obj = (current_time - submission_time)
        com_obj = (current_time - comment_time)
        sub_time = time(sub_obj)
        com_time = time(com_obj)
        #time block

        #Driver Code
        likes = str(comments[j]["comment_likes"])
        comment_author=str(comments[j]["comment_Author"])
        background = Image.open("back.png")
        fonts = glob("*.ttf")
        video_title = Image_Processor()
        title = str(comments[j]["sub_title"])
        video_title.make_title(image=background,title=title,user_name=str(comments[j]["sub_Author"]),time=sub_time,comments=str(comments[j]["sub_comments"]))
        video_main = Image_Processor()
        background = Image.open("back.png")
        profile_picture = Image.open("profile3.png")
        base_image = video_main.base_image(background,profile_picture,comment_author,com_time)
        text = str(comments[j]["Body"]).replace("\n","").replace("’","'").replace("“","\"").replace("/"," ")
        image_making = video_main.adding_text_line_by_line(base_image,text,likes,"750")
        text_to_speech(text.split("."))
        title = title.replace("’","").replace("'","").replace('"','').replace("/"," ")
        tt = title.split(" ")
        tt.extend((f"{j}", "#short-#shorts"))
        vide_name = "-".join(tt)
        make_video(vide_name)
        total_videos.append(vide_name)
        k=k+1
        j+=1
        os.system("clear")
        print(f"Total Videos Made = {k}")
        

    comments.clear()

sel.upload()

       
