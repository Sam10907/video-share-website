import urllib.request as req
import json
import pymysql

conn=pymysql.connect(host='localhost',user='debian-sys-maint',password='vSEM9dkpWNEbj0mf',db='ShareFilm',port=3306,charset='utf8mb4')
cursor=conn.cursor()  #連線資料庫
header={'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
topicId=['','%2Fm%2F02vxn','%2Fm%2F01k8wb','%2Fm%2F06ntj','%2Fm%2F018w8','%2Fm%2F02jjt','%2Fm%2F019_rr','%2Fm%2F05qt0','%2Fm%2F02wbm','%2Fm%2F07c1v']
kinds=['全部','電影','知識','運動','籃球','娛樂','生活','政治','食物','科技']
api_key='AIzaSyDRjZPQPw8OcIqWAdPdlM9l02r-qrnMFBM'
root_url='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&order=rating&type=video&videoDefinition=high&videoDuration=medium&videoEmbeddable=true&key='+api_key
for i in range(0,len(topicId)):
    if i==0:
        request=req.Request(root_url,headers=header)
        with req.urlopen(request) as response:
            data=json.load(response)
        for i1 in range(0,20):
            title=data['items'][i1]['snippet']['title']
            image_url=data['items'][i1]['snippet']['thumbnails']['medium']['url']
            video_id=data['items'][i1]['id']['videoId']
            description=data['items'][i1]['snippet']['description']
            kind=kinds[i]
            cursor.execute("insert into film(title,image_url,video_id,kind,description) values(%s,%s,%s,%s,%s)",(str(title),str(image_url),str(video_id),str(kind),str(description)))
    else:
        urls='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&order=rating&topicId='+topicId[i]+'&type=video&videoDefinition=high&videoDuration=medium&videoEmbeddable=true&key='+api_key
        request=req.Request(urls,headers=header)
        with req.urlopen(request) as response:
            data=json.load(response)
        for i1 in range(0,20):
            title=data['items'][i1]['snippet']['title']
            image_url=data['items'][i1]['snippet']['thumbnails']['medium']['url']
            video_id=data['items'][i1]['id']['videoId']
            description=data['items'][i1]['snippet']['description']
            kind=kinds[i]
            cursor.execute("insert into film(title,image_url,video_id,kind,description) values(%s,%s,%s,%s,%s)",(str(title),str(image_url),str(video_id),str(kind),str(description)))
conn.commit()