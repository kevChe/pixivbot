from pixivpy3 import *
import requests
import shutil
from dotenv import load_dotenv
import os

#load environment
load_dotenv()
PIXIV_REFRESH_TOKEN = os.getenv('PIXIV_REFRESH_TOKEN')

#Setup pixivpy api
api = AppPixivAPI()
api.auth(refresh_token=PIXIV_REFRESH_TOKEN)

def search(query):
    json_result = api.search_illust(query, search_target="partial_match_for_tags", sort="popular_desc")
    # for illust in json_result.illusts:
    #     print(illust.meta_single_page.original_image_url)
    return json_result.illusts

def get_details(number):
    json_result = api.illust_detail(number)
    illust = json_result.illust

    if len(illust.meta_pages) == 0:
        url = [illust.meta_single_page.original_image_url]
    else:
        # url = [url['image_urls']['original'] for url in illust.meta_pages]
        url = [url.image_urls.original for url in illust.meta_pages]
        # url = illust.meta_pages

    tags = [tag.name for tag in illust.tags]
    r18 = False
    for tag in tags:
        if tag == 'R-18':
            r18 = True
    return {
        "url": url,
        "r18": r18,
        "like": illust.total_bookmarks
    }

def download_pic(url):
    headers = {
        'referer': 'https://www.pixiv.net/',
    }

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        local_filename = url.split('/')[-1]
        with open(local_filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        print(local_filename)
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


for illust in search("hololive 0000"):
    # detail = get_details(illust)
    print(get_details(illust.id))

# print(get_details(117552279))
# print(get_details(117860622))



# json_result = api.illust_recommended()
# for illust in json_result.illusts:
#     print(f"https://www.pixiv.net/artworks/{illust.id}")


# get ranking: 1-30
# mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
# json_result = api.illust_ranking('day')
# for illust in json_result.illusts:
#     print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

# # next page: 31-60
# next_qs = api.parse_qs(json_result.next_url)
# json_result = api.illust_ranking(**next_qs)
# for illust in json_result.illusts:
#     print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))

# # get all page:
# next_qs = {"mode": "day"}
# while next_qs:
#     json_result = api.illust_ranking(**next_qs)
#     for illust in json_result.illusts:
#         print("[%s] %s" % (illust.title, illust.image_urls.medium))
#     next_qs = api.parse_qs(json_result.next_url)


# url = 'https://i.pximg.net/img-master/img/2021/10/07/19/41/28/93284987_p0_master1200.jpg'
# url = 'https://i.pximg.net/img-original/img/2021/06/08/16/07/43/90413231_p0.jpg'
