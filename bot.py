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
    s = re.findall(r'_sharedData = ([^&]*);</sc', r.text)[0]
    s = re.findall(r'([^&]*);</sc', res)[0]
    jsonObj = json.loads(s)
    cursor = jsonObj['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    
    return cursor

def getTagImgId(tag, token, cursor, count):
    url = 'https://www.instagram.com/explore/tags/'+tag+'/'
    data = dict(csrfmiddlewaretoken=token)
    r = client.get(url, data=data, headers=dict(Referer=url))
    r = client.get(url, data=data, headers=dict(Referer=url))
    s = re.findall(r'_sharedData = ([^&]*);</sc', r.text)[0]
    s = re.findall(r'([^&]*);</sc', res)[0]
    mediaId = jsonObj['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']
    
    return mediaId

def like(tagArray, token):
    count = 0
    while True:
        for tag in tagArray:
            random_tag = random.choice(arrayTag)
            print 'Current tag: ' +random_tag
            cursor = getEndCursor(random_tag, token)
            imgId = getTagImgId(random_tag, token, cursor, countImg)
            
            data = dict(csrfmiddlewaretoken=token, Domain='.instagram.com')
            for i in imgId:
                timeDelay = random.choice(randomTime)
                print 'Current delay: ' + str(timeDelay)
                time.sleep(timeDelay)
                url = 'https://www.instagram.com/web/likes/'+ str(i['node']['id']) +'/like/'
                r = client.post(url, data=data, headers=dict(Referer='https://www.instagram.com/web/'))
                print r.text
                count += 1
                print count

client = requests.session()
csrftoken = login(username, password)

like(arrayTag, csrftoken)
