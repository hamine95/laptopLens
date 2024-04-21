import datetime
import json
import requests
from dateutil import parser
import pytz

def main():
    url="https://api.ouedkniss.com/graphql"
    general_header={"authorization": None, "locale": "fr", "x-app-version": "\"3.0.8\"", "x-referer": "https://www.ouedkniss.com/informatique-ordinateur-portable-laptop/1"}
    is_current_year=True
    page_count=1
    num_per_page=50
    announcemnts=[]
    while is_current_year:

        search_payload={"operationName":"SearchQuery","variables":{"mediaSize":"MEDIUM","q":None,"filter":{"categorySlug":"informatique-ordinateur-portable-laptop","origin":None,"connected":False,"delivery":None,"regionIds":[],"cityIds":[],"priceRange":[None,None],"exchange":False,"hasPictures":False,"hasPrice":False,"priceUnit":None,"fields":[],"page":page_count,"count":num_per_page}},"query":"query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      filter {\n        cities {\n          id\n          name\n          __typename\n        }\n        regions {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}"}
        result=requests.post("https://api.ouedkniss.com/graphql", json=search_payload, headers=general_header)
        #result=requests.post(url,json=page_payload,headers=general_header)
        print(f'page num:{page_count} status:{result.status_code}')
        
        data=result.json()
        #print(data["data"]["search"]["announcements"]["data"])
        data=data["data"]["search"]["announcements"]["data"]
        print(len(data))
        
        for j,reslt in enumerate(data):
            
            id=reslt['id']
            title=reslt['title']
            slug=reslt['slug']
            isFromStore=reslt['isFromStore']
            userReaction=reslt['userReaction']
            created_date=parser.parse(reslt['createdAt'])
            print(f"annoncement num:{j} date:{created_date}")
            announcement_get={"operationName":"AnnouncementGet","variables":{"id":id},"query":"query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    oldPricePreview\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      id\n      slug\n      name\n      deliveryType\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      parentId\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      announcementsCount\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      pricePreview\n      oldPricePreview\n      quantity\n      __typename\n    }\n    showAnalytics\n    messengerLink\n    __typename\n  }\n}"}
            get_post=requests.post("https://api.ouedkniss.com/graphql", json=announcement_get, headers=general_header)
            get_post=get_post.json()
            get_post=get_post["data"]["announcement"]
            specs=get_post['specs']
            anon={}
            anon["cpu"]=False
            anon["ram"]=False
            anon["disctype"]=False
            for spec in specs:
                if "Processeur" in spec["specification"]["label"]:
                    anon["cpu"]=True
                if "RAM" in spec["specification"]["label"]:
                    anon["ram"]=True
                if "Type disque" in spec["specification"]["label"]:
                    anon["disctype"]=True
            announcemnts.append(anon)
            before_datetime=datetime.datetime(2024,1,1,1,0,0,0,(pytz.utc))
            if created_date<before_datetime:
                is_current_year=False
                break

        page_count+=1
        break
    print(f'cpu specified:{len([anc for anc in announcemnts if anc["cpu"]])}/{len(announcemnts)}')
    print(f'ram specified:{len([anc for anc in announcemnts if anc["ram"]])}/{len(announcemnts)}')
    print(f'disctype specified:{len([anc for anc in announcemnts if anc["disctype"]])}/{len(announcemnts)}')
    print(f'all 3 data specified:{len([anc for anc in announcemnts if anc["disctype"] and anc["cpu"] and anc["ram"]])}/{len(announcemnts)}')





if __name__ == "__main__":
    main()