import requests
import pandas as pd
import time
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
API_KEY = "YOUR API KEY"

def get_channel_id(query):
    youtube_link = ""
    for result in search(query, tld="co.in", num=10, stop=10, pause=2):
        if("www.youtube.com" in result):
            youtube_link = result
            break
    channel_id = result.split("www.youtube.com")[1]
    if("channel" in channel_id):
        channel_id = channel_id.split("/channel/")[1]
    else:
        username = channel_id.split("/c/")[1]
        username = username.split("/")[0]
        pageToken = ""
        url = 'https://www.googleapis.com/youtube/v3/channels?key='+API_KEY+"&forUsername="+username+"&part=contentDetails"+pageToken
        response = requests.get(url).json()
        channel_id = response["items"][0]["id"]
    return channel_id

def get_video_details(video_id):        
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats = requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    #dislike_count = response_video_stats['items'][0]['statistics']['dislikeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']
    
    return view_count,like_count,comment_count

def get_comments(video_id):
    comments_list = []
    pageToken = ""
    url = 'https://www.googleapis.com/youtube/v3/commentThreads?key='+API_KEY+"&videoId="+video_id+"&part=snippet,id&textFormat=plainText&maxResults=20"+pageToken
    comments_response = requests.get(url).json()
    for comments_dictionary in comments_response["items"]:
        comment = comments_dictionary['snippet']['topLevelComment']['snippet']['textDisplay']
        comments_list.append(comment)
    return comments_list

def get_statistics(response):
    statistics_df = pd.DataFrame(columns=["video_id","video_title","upload_date","view_count","like_count","comment_count"])
    comments_df = pd.DataFrame(columns=["video_id","video_title","Comments"])
    for video in response['items']:
        if(video['id']['kind'] == "youtube#video"):
            video_id = video["id"]["videoId"]
            video_title = video["snippet"]["title"]
            video_title = str(video_title).replace("&amp;","")
            upload_date = video['snippet']['publishedAt']
            upload_date = str(upload_date).split("T")[0]

            view_count,like_count,comment_count=get_video_details(video_id)
            comments_list = get_comments(video_id)
            for comment in comments_list:
                comments_df = comments_df.append({"video_id":video_id,"video_title":video_title,"Comments":comment}, ignore_index = True)
            statistics_df = statistics_df.append({'video_id':video_id,'video_title':video_title,'upload_date':upload_date,'view_count':view_count,'like_count':like_count,'comment_count':comment_count}, ignore_index = True)
    return statistics_df,comments_df

def get_all_details(query):
    CHANNEL_ID = get_channel_id(query)
    pageToken = ""
    url = 'https://www.googleapis.com/youtube/v3/search?key='+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=20"+pageToken
    channel_response = requests.get(url).json()
    statistics_df,comments_df = get_statistics(channel_response)
    return statistics_df,comments_df

