from apiclient.discovery import build
import pandas as pd
api_key = "AIzaSyCz2nLXAUJ7djd9mNBA05wxuowHRNQrFn4"
# Creating the youtube resource
youtube = build('youtube','v3', developerKey = api_key)

# Definition of all functions
def get_channel_vids(channelid):
    """
    This is a function that returns a list of all the videos on a certain channel.
    """
    a = youtube.channels().list(id=channelid, part='contentDetails').execute()

    playlistid = a['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    nextPageToken = None
    
    while 1:
        res = youtube.playlistItems().list(playlistId=playlistid, part = 'snippet',
                                           maxResults=50, pageToken = nextPageToken).execute()
        videos += res['items']
        nextPageToken = res.get('nextPageToken')
        
        if nextPageToken is None:
            break
    return videos

def get_topchanel_channel_ids():
    """
    This is a function that returns a list of 200 most popular 
    gaming the channels.
    """
    channel_ids_raw = []
    nextPageToken = None
    
    while 1:
        a = youtube.videos().list(part = 'snippet', chart = 'mostPopular', 
                            regionCode='US', videoCategoryId = '20',
                            maxResults = 50, pageToken = nextPageToken).execute()
        for i in range(len(a['items'])):
            channel_ids_raw.append(a['items'][i]['snippet']['channelId'])
        
        nextPageToken = a.get('nextPageToken')
        
        if nextPageToken is None:
            break
    return channel_ids_raw

def get_ids(video_list):
    """
    Return the list fo videos id's.
    """
    return list(map(lambda x:x['snippet']['resourceId']['videoId'], video_list))

def get_statistics_vids(id_lists, 
                        stat_request = 'snippet,statistics,topicDetails,contentDetails'):
    """
    This will return several statistics for videos. As a defualt it will get the statistics, 
    topic relations, snippets.
    """
    stats = []
    for i in range(0,len(id_lists), 50):
        request = youtube.videos().list(id=','.join(id_lists[i:i+50]),
                                       part = stat_request).execute()
        stats += request['items']
    return stats

def unique(list1): 
    """
    This function will return the unique values of a list
    """
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

# we are starting with the most popular videos on the gaming channel
raw_channel_ids = get_topchanel_channel_ids()

# Now lets get all the unique values 
channelid_list = unique(raw_channel_ids)

# This is all the null lists that will be transformed in a data frame later
title,description,likes,dislikes,topic_raw,topic,comments,views = [],[],[],[],[],[],[],[]
vid_duration,channel_title,vid_category,published_date = [],[],[],[]
channelid,subcribercount,totalvids,totalviews = [],[],[],[]

# Main loop
for chanelid in channelid_list:
    # Get the main statistics from the channel
    req2 = youtube.channels().list(id = chanelid, part = 'snippet,statistics,topicDetails', maxResults = 5).execute()
    channeltitle = req2['items'][0]['snippet']['title']
    total_views = int(req2['items'][0]['statistics']['viewCount'])
    totalsubscribers = int(req2['items'][0]['statistics']['subscriberCount'])
    total_vids = int(req2['items'][0]['statistics']['videoCount'])
    
    # Get the video data from the playlist
    videos = get_channel_vids(chanelid)
    
    # Get the ids of those videos
    ids = get_ids(videos)
    
    # Get the raw statistics
    stats = get_statistics_vids(ids)
    for i in range(len(stats)):
    # Adding 
        channelid.append(chanelid)
        subcribercount.append(totalsubscribers)
        totalvids.append(total_vids)
        totalviews.append(total_views)
        # Performing the necesary checks per video
        stats_check,topic_check,content_check,stats_check_like,stats_check_view = 0,0,0,0,0
        stats_check_dislikes, stats_check_view_comments = 0,0
        for name, data in stats[i].items():
            if 'statistics' in name:
                for a,b in stats[i]['statistics'].items():
                    if 'likeCount' in a:
                        stats_check_like = 1
                    if 'viewCount' in a:
                        stats_check_view = 1
                    if 'dislikeCount' in a:
                        stats_check_dislikes = 1
                    if 'commentCount' in a:
                        stats_check_view_comments = 1
            if 'topicDetails' in name:
                for a,b in stats[i]['topicDetails'].items():
                    if 'relevantTopicIds' in a:
                        topic_check = 1
            if 'contentDetails' in name:
                content_check = 1
        # 1st we load snippet, that all should have
        title.append(stats[i]['snippet']['title']) 
        description.append(stats[i]['snippet']['description'])
        channel_title.append(stats[i]['snippet']['channelTitle'])
        vid_category.append(int(stats[i]['snippet']['categoryId']))
        published_date.append(stats[i]['snippet']['publishedAt'])
        if stats_check_dislikes == 1:
            dislikes.append(int(stats[i]['statistics']['dislikeCount']))
        elif stats_check_dislikes == 0:
            dislikes.append(['NaN'])
        if stats_check_view_comments == 1:
            comments.append(int(stats[i]['statistics']['commentCount']))
        elif stats_check_view_comments == 0:
            comments.append(['NaN'])
        if stats_check_like == 1:
            likes.append(int(stats[i]['statistics']['likeCount']))
        elif stats_check_like == 0:
            likes.append(['NaN'])
        if stats_check_view == 1:
            views.append(int(stats[i]['statistics']['viewCount']))
        elif stats_check_view == 0:
            views.append(['NaN'])
        if topic_check == 1:
            topic_raw.append(stats[i]['topicDetails']['relevantTopicIds'])
        elif topic_check == 0:
            topic_raw.append(['NaN'])
        if content_check == 1:
            vid_duration.append(stats[i]['contentDetails']['duration'])
        elif content_check == 0:
            vid_duration.append(['NaN'])

# Pre-processing unique values of topic
topic = []
for i in range(len(topic_raw)):
    topic.append(unique(topic_raw[i]))

# Set all the data as a pandas Data Frame
df = pd.DataFrame(list(zip(title,description,likes,dislikes,topic,comments,views,
                          vid_duration,channel_title,vid_category,
                          channelid,subcribercount,totalvids,totalviews,published_date)), 
                  columns =['vid_title','vid_description','vid_likes',
                           'vid_dislikes','vid_related_topic','vid_comments','vid_views',
                           'vid_duration','channel_title','vid_category',
                           'channelid','subcriber_count','chanel_num_vids','chanel_total_views',
                           'published_date']) 

# Saving the data as a csv file or some file type that R can read: csv and json files.