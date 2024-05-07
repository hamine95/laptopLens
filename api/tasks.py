import logging
from celery import shared_task

import datetime
import requests
import json
from dateutil import parser
from .models import Announcement
from .models import Ram, CPU, Disc, Laptop, Store, Location
import ollama

page_count=1
num_per_page=50
url="https://api.ouedkniss.com/graphql"
general_header={"authorization": None, "locale": "fr", "x-app-version": "\"3.0.8\"", "x-referer": "https://www.ouedkniss.com/informatique-ordinateur-portable-laptop/1"}
search_payload={"operationName":"SearchQuery","variables":{"mediaSize":"MEDIUM","q":None,"filter":{"categorySlug":"informatique-ordinateur-portable-laptop","origin":None,"connected":False,"delivery":None,"regionIds":[],"cityIds":[],"priceRange":[None,None],"exchange":False,"hasPictures":False,"hasPrice":False,"priceUnit":None,"fields":[],"page":page_count,"count":num_per_page}},"query":"query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      filter {\n        cities {\n          id\n          name\n          __typename\n        }\n        regions {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}"}
announcement_get={"operationName":"AnnouncementGet","variables":{"id":""},"query":"query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    oldPricePreview\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      id\n      slug\n      name\n      deliveryType\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      parentId\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      announcementsCount\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      pricePreview\n      oldPricePreview\n      quantity\n      __typename\n    }\n    showAnalytics\n    messengerLink\n    __typename\n  }\n}"}


def post_json_result(url,payload,headers):
    result=requests.post(url, json=payload, headers=headers)
    return result.json()


def get_pc_specs(json_result):
    specs=json_result['specs']
    anon={}
    spec_list=["processeur","ram","disque_type","disque","etat","ecran","marque"]
    specs_found=0
    anon["specs_specified"]=False
    for spec in specs:
        if any(x_spec in spec["specification"]["codename"] for x_spec in spec_list):
            spec_codename=spec["specification"]["codename"]
            anon[spec_codename]=spec["valueText"][0]
            specs_found+=1
        if specs_found == len(spec_list):
            anon["specs_specified"]=True
    return anon

def get_store(json_result):
    store=json_result['store']
    store_model={}
    store_keys=["name","slug","description","imageUrl","url","followerCount","announcementsCount"]

    if "name" in store:
        store_model["name"]=store["name"]
    if "slug" in store:
        store_model["slug"]=store["slug"]
    if "description" in store:
        store_model["description"]=store["description"]
    if "imageUrl" in store:
        store_model["imageUrl"]=store["imageUrl"]
    if "url" in store:
        store_model["url"]=store["url"]
    if "followerCount" in store:
        store_model["followerCount"]=store["followerCount"]
    if "announcementsCount" in store:
        store_model["announcementsCount"]=store["announcementsCount"]
    store_model["location"]=None
    if "locations" in store:
        if len(store["locations"])>0:
            store_model["location"]={}
            store_model["location"]["address"]=store["locations"][0]["location"]["address"]
            store_model["location"]["wilaya"]=store["locations"][0]["location"]["region"]["name"]
        
    return store_model


def get_announcement_details(announcement):
    id=get_announcement_id(announcement)
    created_date=get_announcement_date(announcement)
    like_count=get_announcement_likes(announcement)
    title=get_announcement_title(announcement)
    description=get_announcement_description(announcement)
    has_delivery=announcement.get("has_delivery")
    price=announcement.get("price")
    if not price:
        price=1
    return {"id":id,"created_date":created_date,"like_count":like_count,"title":title
            ,"description":description,"has_delivery":has_delivery,"price":price}



def get_announcement_id(announcement):
    return announcement['id']

def get_announcement_date(announcement):
    created_date=parser.parse(announcement['createdAt'])
    return created_date

def get_announcement_likes(announcement):
    like_count=announcement['likeCount']
    return like_count


def get_announcement_title(announcement):
    title=announcement['title']
    return title


def get_announcement_description(announcement):
    description=announcement['description']
    return description


def set_announcement_id(id):
    announcement_get["variables"]["id"]=id
    return announcement_get

def get_page_data(json_result):
    return json_result["data"]["search"]["announcements"]["data"]

def get_announcement_data(json_result):
    return json_result["data"]["announcement"]


def is_from_store(json_result):
    return json_result['isFromStore']

def get_cpu(cpu):
    return CPU.add_new_cpu(cpu)

def get_ram(ram):
    return Ram.add_new_ram(ram)

def get_disc(disc,disc_type):
    return Disc.add_new_disc(disc,disc_type)

def create_laptop(laptop):
    new_laptop={}
    new_laptop["ram"]=get_ram(laptop["ram"])
    new_laptop["cpu"]=get_cpu(laptop["processeur"])
    new_laptop["disc"]=get_disc(laptop["disque"],laptop["disque_type"])
    new_laptop["brand"]=laptop["marque"]

    return Laptop.add_new_laptop(brand=new_laptop["brand"], ram=new_laptop["ram"], 
                          cpu=new_laptop["cpu"], disc=new_laptop["disc"])


def get_location(location):
    if location==None:
        return None
    return Location.add_new_location(location["address"], location["wilaya"])


def get_images(data):
    medias=[]
    for media in data["medias"]:
        medias.append(media["mediaUrl"])
    return medias

def create_store(store):
    new_store={}
    new_store["name"]=store["name"]
    new_store["slug"]=store["slug"]
    new_store["description"]=store["description"]
    new_store["image_url"]=store["imageUrl"]
    new_store["url"]=store["url"]
    new_store["followers"]=store["followerCount"]
    new_store["annoncement_count"]=store["announcementsCount"]
    new_store["locations"]=get_location(store["location"])
    return Store.add_new_store(new_store["name"],new_store["slug"],new_store["description"],new_store["locations"],
                               new_store["image_url"],new_store["url"],new_store["followers"]
                               ,new_store["annoncement_count"])


def save_new_announcement(announcement_data):
    laptop=create_laptop(announcement_data["laptop"])
    store=None
    if announcement_data["store"]:
        store=create_store(announcement_data["store"])
    
    if announcement_data["announcement"]["has_delivery"]==None:
        announcement_data["announcement"]["has_delivery"]=False
    else:
        announcement_data["announcement"]["has_delivery"]=True
    new_announcement=Announcement(announcement_data["announcement"]["id"],laptop=laptop,store=store,
                                               title=announcement_data["announcement"]["title"],
                                               created_at=announcement_data["announcement"]["created_date"],
                                               like_count=announcement_data["announcement"]["like_count"],
                                               description=announcement_data["announcement"]["description"],
                                               has_delivery=announcement_data["announcement"]["has_delivery"],
                                               price=announcement_data["announcement"]["price"],
                                               medias=announcement_data["medias"],
                                               )
    
    new_announcement.save()


def get_recent_announcement_date():
    latest_announcement={"created_at":0}
    if Announcement.objects.exists() > 0:
        latest_announcement= Announcement.objects.values('created_at').latest('created_at')
    return latest_announcement['created_at']

def has_been_added(created_date,recent_anon_date):
    if recent_anon_date==0:
        return False
    return created_date <= recent_anon_date




def ask_ollama(msg):
    response = ollama.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': f'extract specs of this laptop and give me output in json format: {msg}',
    },
    ])
    logging.info(response['message']['content'])


@shared_task(name="get_new_announcements")
def get_new_announcements():
    
    announcemnts=[]
    json_result=post_json_result(url,search_payload,general_header)
    data=get_page_data(json_result)
    recent_annoncement_date=get_recent_announcement_date()
    logging.info(f"recent_annoncement_date: {recent_annoncement_date}")

    for j,announcement in enumerate(data):
        announcement_model=get_announcement_details(announcement)
        logging.info(f"announcement created date: {announcement_model['created_date']}")
        
        if has_been_added(created_date=announcement_model['created_date'],recent_anon_date=recent_annoncement_date):
            logging.info("already exist in database")
            break
        announcement_payload=set_announcement_id(announcement_model['id'])
        json_result=post_json_result(url,announcement_payload,general_header)
        announcement_data=get_announcement_data(json_result)
        announcement_images=get_images(announcement_data)
        laptop_specs=get_pc_specs(announcement_data)
        store_data=None
        if is_from_store(announcement_data):
            store_data=get_store(announcement_data)
        announcement_info={"announcement":announcement_model,"laptop":laptop_specs,"store":store_data,"medias":announcement_images}
        announcemnts.append(announcement_info)
        # ask_ollama(announcement_model["description"])
        
        logging.info('****************************************')
        logging.info(f'{j} announcement general: {announcement_info["announcement"]["title"]}')
        logging.info(f'announcement laptop: {announcement_info["laptop"]["specs_specified"]}')
        if is_from_store(announcement_data):
            logging.info(f'announcement store: {announcement_info["store"]["name"]}')
        logging.info('****************************************')
        if announcement_info["laptop"]["specs_specified"]:
            save_new_announcement(announcement_info)

    logging.info(f'announcements with all specs: {len([announcement for announcement in announcemnts if announcement["laptop"]["specs_specified"]])} ')
    logging.info(f'announcements missing specs: {len([announcement for announcement in announcemnts if not announcement["laptop"]["specs_specified"]])} ')






