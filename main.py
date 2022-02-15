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

class Image_Processor:
    
    def __init__(self):
        pass
    
    #Function to make title png & audio
    def make_title(self,image,title,user_name,time,comments):
        
        print(title)
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
    
    #Function to make text to speech uing pyttsx3 

    # Fuction to draw a line in an image
    def draw_line(self,image, height):
        draw = ImageDraw.Draw(image)
        draw.line((65, 390, 65, 390+height),width=3, fill=(157,157,163))
        return image 
    
    # Fuction to add text to an image
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
        
    # Fuction to add multiline text to an image
    def add_multiline_text(self,image, text, color,font,position):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, size=35)
        draw.text(position, text, fill=color, font=font)
        # draw.multiline_textbbox(position, text, font=font)
        font_width,font_height = draw.textsize(text, font=font)
        print(font_width,font_height)
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
        while(i<len(split)):
            
            # if i==len(split):
            #     image = self.add_image()
            word_list = wrapper.wrap(text=split[i].strip()+".")
            # print(f"{i} = Word List => {word_list}")
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
            
# Fuction to convert text to speech using google text to speech
def text_to_speech(texts):
    i=1
    print(texts)
    print(len(texts))
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')[7]
    engine.setProperty('voice', voice.id)
    for text in texts:
        print(f"Sending text to speech {text}")
        engine.save_to_file(text, f"test{i}.mp3")
        print(f"Saved text to speech {text}")
        i=i+1
    engine.runAndWait()
    print("Done")
    
    

# Function to join image to audio using ffmpeg
def make_video(name:str):
    # print(images)
    audios = glob("test*.mp3")
    images = glob("test*.png")
    j = random.randint(0,10)
    i=0
    while i<len(audios):
        # os.system(f"echo 'file test{i}.mp3' >> audio.txt")
        # os.system(f"echo 'file test{i}.png' >> image.txt")
        os.system(f"ffmpeg  -i test{i}.png -i test{i}.mp3 -c:a aac -vcodec libx264 test{i}.mp4")
        # os.system(f"ffmpeg -loop 1 -i test{i}.png -i test{i}.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest text{i}.mp4")
        i=i+1
    print("Done")
    print("compiling video")
    videos = glob("test*.mp4")
    i=0
    videos.sort()
    print(videos)
    while i<len(videos):
        os.system(f"echo 'file test{i}.mp4' >> list.txt")
        i=i+1
        
    os.system(f"ffmpeg -f concat -safe 0 -i list.txt -c copy videos/{name}.mp4")
    # os.system(f"rm list.txt && rm audio.txt && rm image.txt")


    # Function to get the title of the post

    
    
#Function to upload video to youtube using youtube data api
# def upload_video(video_name:str,title:str):
#     description = "Subscribe for more funny and awesome videos thought the day #shorts #reddit"
#     title = title + "#shorts"
#     key = "funny,reddit,fun,cool,askreddit"
#     os.system(f'python /Users/ipriyam26/Programing/Reddit TTS/upload_video.py --file="{vide_name}.mp4" --title="{title}" --description="{description}" --key="{key}" --category="22" --privacy="public"')
#     os.system(f"rm {video_name}.mp4")
    # python /Users/ipriyam26/Programing/Reddit TTS/upload_video.py --file="output.mp4"
#                        --title="New SUper Funny video"
#                        --description="check out now and like and subscribe"
#                        --keywords="funny,cute,laugh"
#                        --category="22"
#                        --privacyStatus="private"        

# im = Image.open("back.png")
# ttf = glob("*.ttf")
# profile = Image.open("profile3.png")
# process = Image_Processor()
# title = "What is one thing COVID has taken away that we’ll never get back?"
# # process.add_title(im,title,"ipriyam26","3 years","21.0k").show()
# process.make_title(image=im,title=title,user_name="ipriyam26",time="3 years",comments="21.0k")

# plan = Image_Processor()
# im= Image.open("back.png")
# im = process.base_image(im,profile,"TheJimDim",time = "3 years")
# # im = process.add_multiline_text(im,text , (255, 0, 0),font=ttf[1],position=(130,65))
# text = "I had this hot roommate that did those princess parties things where you dress up as a Disney Princess and go to birthday parties.  \n\nOne day I come home and I’m headed to my room and she’s about to head out to a princess party. She steps out in full Snow White gear, wig, ruby red lipstick, etc. She turns around and points to her back.\n“Hey can you help me with this zipper?”  I didn’t think I’d be turned on by a Disney princess. And Snow White of all people. \n\nRunner up, I’ve never been into the whole… dom/sub thing. Until I was with a chick who was into it and I didn’t realize til I told her to do something while in bed and she replied with a yes, sir."

# text = text.replace("’","'").replace("\n","")
# tt = title.split(" ")
# vide_name = "-".join(tt)
# pp = plan.adding_text_line_by_line(im,text,"12k","102")

# text_to_speech(text.split("."))
# make_video(vide_name)
# print(pp)
# sk = "I shower once a week. Sometimes I go longer. I also have"
# print(len(sk))


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
reddit = praw.Reddit(client_id='k_ZnJdAJyM-NRNjOJhfJJw',
                     client_secret='zr3sjutLDNyEi6gFSd4eZ-gqAb9nUw',
                     user_agent='android:com.example.myredditapp:v1.0.0 (by /u/Fantastic-Apartment8)',
                     username='Fantastic-Apartment8',
                     password='mcsx007A')
                     
print(reddit.read_only)
subreddit = reddit.subreddit('AskReddit')
# subreddit.top(limit=10)
submissions = subreddit.hot(limit=100)
s = int(input("How many videos do you want to make? "))
k=0
subIds=[submission.id for submission in submissions]
print(len(subIds))
os.system("rm -rf videos")
os.system("mkdir videos")

while k<s:
    comments=[]
    p=1
    f=0
    for subID in subIds:
        submission = reddit.submission(id=subID)
        print(submission.title)
        
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
                    print(comment)
                    comments.append(comment)
                    
            except: 
                print("NO MORE IN THIS SUBMISSION")
                p+=1
                
        subIds = subIds[p:]        
                      
        if(f==1):
            break   
    
    j=0
    while j<len(comments):
       
        #time block
        current_time = datetime.now().timestamp()
        submission_time = float(comments[j]["sub_time"])
        print(current_time-submission_time)
        comment_time = float(comments[j]["comment_time"])
        sub_obj = (current_time - submission_time)
        com_obj = (current_time - comment_time)
        print(sub_obj)
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
        text = str(comments[j]["Body"]).replace("\n","").replace("’","'")
        image_making = video_main.adding_text_line_by_line(base_image,text,likes,"750")
        text_to_speech(text.split("."))
        title = title.replace("’","").replace("'","").replace('"','')
        tt = title.split(" ")
        tt.append(f"{j}")
        tt.append("#short-#shorts")
        vide_name = "-".join(tt)
        make_video(vide_name)
        k=k+1 
        j+=1
        os.system("rm list.txt")
        for image in glob("test*.png"):
            os.system(f"rm {image}")
        for audio in glob("test*.mp3"):
            os.system(f"rm {audio}")   
        for vid in glob("test*.mp4"):
            os.system(f"rm {vid}")       
    comments.clear()
       
