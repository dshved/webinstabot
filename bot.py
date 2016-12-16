#!/usr/bin/python
# -*- coding: utf-8 -*- 
# coding: utf8
import sys
import requests
import json
import re
import random
import time

username = 'USERNAME'
password = 'PASSWORD'

arrayTag = ['welltravelled', 'exploremore', 'exklusive_shot', 'photo_russia',
            'madrussians', 'russian_inspiration', 'photorussia', 'instarussia',
            'gf_russia','russiandiary','russia_ww','russia','natgeoru','vscorussia',
            'instagramrussia','VSCOGoodShot', 'mobilemag','wanderfolk','diewocheaufinstagram','vscocam',
            'LiveTravelChannel','achadosdasemana','ig_russia','thisismycommunity',
            'outsideisfree','letsgosomewhere','cntravellerrussia','Crimeaphoto','urban',
            'Photoday','Crimea','snapseed','vsco','vscorus','bestofvsco','vscocrimea',
            'vscostyle','vscofeature','canon_photos','natureaddict','hallazgosemanal',
            'lifeofadventure','wildernessculture','realfolklife','visualsoflife',
            'peoplescreatives','folktravel','exploringtheglobe','FolkGood','liveauthentic',
            'exploretocreate','folkmagazine','livefolk','ig_photooftheday','featuremeinstagood']

randomTime = [24,27,31,35,38,41,44,51,59]

countImg = 20

def login(username, password):
    url = 'https://www.instagram.com/accounts/login/?force_classic_login=&next='
    ref_url = 'https://www.instagram.com'

    client.get(url)
    csrftoken = client.cookies['csrftoken']
    
    login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken, next=ref_url)
    r = client.post(url, data=login_data, headers=dict(Referer=url))
    token = r.cookies['csrftoken']
    
    return token
    
def getEndCursor(tag, token):
    url = 'https://www.instagram.com/explore/tags/'+tag+'/'
    data = dict(csrfmiddlewaretoken=token)
    r = client.get(url, data=data, headers=dict(Referer=url))
    html = r.text
    jsonObj = json.loads(re.findall(r'_sharedData = ([^&]*);</sc', html)[0])
    cursor = jsonObj['entry_data']['TagPage'][0]['tag']['media']['page_info']['end_cursor']
    return cursor

def getTagImgId(tag, token, cursor, count):
    tag_url = 'https://www.instagram.com/query/'
    img_url = 'https://www.instagram.com/explore/tags/'+tag+'/'
    query = "ig_hashtag("+ tag +") { media.after("+ cursor +", "+ str(count) +") {count,nodes {id},page_info}}"
  
    data = dict(csrfmiddlewaretoken=token, q=query, ref='tags::show')
    r = client.post(tag_url, data=data, headers=dict(Referer=img_url))
    jsonObj = json.loads(r.text)
    mediaId = jsonObj['media']['nodes']
    return mediaId

def like(tagArray, token):
    while True:
        for tag in tagArray:
            random_tag = random.choice(arrayTag)
            print 'Current tag: ' +random_tag
            cursor = getEndCursor(random_tag, token)
            imgId = getTagImgId(random_tag, token, cursor, countImg)
            data = dict(csrfmiddlewaretoken=token)
            for i in imgId:
                timeDelay = random.choice(randomTime)
                print 'Current delay: ' + str(timeDelay)
                time.sleep(timeDelay)
                url = 'https://www.instagram.com/web/likes/'+ str(i['id']) +'/like/'
                r = client.post(url, data=data, headers=dict(Referer='https://www.instagram.com/web/'))
                print r.text  

client = requests.session()
csrftoken = login(username, password)

like(arrayTag, csrftoken)