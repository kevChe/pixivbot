from pixivpy3 import *
import requests
import shutil
from dotenv import load_dotenv
import os
from db import DB

class Pixiv_scrape():

    COLLECTION = 'links'

    def __init__(self) -> None:
        #load environment
        load_dotenv()
        PIXIV_REFRESH_TOKEN = os.getenv('PIXIV_REFRESH_TOKEN')

        #Setup pixivpy self.api
        self.api = AppPixivAPI()
        self.api.auth(refresh_token=PIXIV_REFRESH_TOKEN)

    def search(self, query, offset):
        json_result = self.api.search_illust(query, search_target="partial_match_for_tags", offset=offset, sort="date_asc" )
        return json_result.illusts

    def get_details(self, number):
        json_result = self.api.illust_detail(number)
        illust = json_result.illust
        # print(illust)
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
            "like": illust.total_bookmarks,
            "id": illust.id
        }

    @staticmethod
    def download_pic(url, local_filename):
        headers = {
            'referer': 'https://www.pixiv.net/',
        }

        response = requests.get(url, headers=headers, stream=True)

        if response.status_code == 200:
            with open(local_filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print(local_filename)
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

def main():
    
    # Loop code to scrape website from search


    ps = Pixiv_scrape()
    db = DB()
    # doc = {"r18": True, "url": "byedasdfbye"}
    # db.insert(doc)


    stop = False
    offset = 172
    count = offset
    keyword = "hololive"
    min_likes = "000"

    try:
        while not stop:
            print(offset)
            search = ps.search(f"{keyword} {min_likes}", offset)
            for illust in search:
                detail = ps.get_details(illust.id)
                url = detail['url'][0]
                likes = detail['like']
                r18 = detail['r18']
                id = detail['id']
                print(f"{id}  {url} {likes} {r18} {count}")
                doc = {"_id": id, "url": url, "likes": likes, "r18": r18, "count": count, "tag": keyword}
                db.insert(doc)
                count += 1
            if len(search) == 0:
                stop = True
            offset += 30
    except TypeError as e:
        print("Type Error, connection might have lost, please try again later")
    except AttributeError as e:
        print("Attribute Error, maximum number of retrieval reached")

    db.close()


if __name__ == "__main__":
    main()

    # print(get_details(117552279))
    # print(get_details(117860622))



    # json_result = self.api.illust_recommended()
    # for illust in json_result.illusts:
    #     print(f"https://www.pixiv.net/artworks/{illust.id}")          


    # get ranking: 1-30
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # json_result = self.api.illust_ranking('day')
    # for illust in json_result.illusts:
    #     print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

    # # next page: 31-60
    # next_qs = self.api.parse_qs(json_result.next_url)
    # json_result = self.api.illust_ranking(**next_qs)
    # for illust in json_result.illusts:
    #     print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))

    # # get all page:
    # next_qs = {"mode": "day"}
    # while next_qs:
    #     json_result = self.api.illust_ranking(**next_qs)
    #     for illust in json_result.illusts:
    #         print("[%s] %s" % (illust.title, illust.image_urls.medium))
    #     next_qs = self.api.parse_qs(json_result.next_url)


    # url = 'https://i.pximg.net/img-master/img/2021/10/07/19/41/28/93284987_p0_master1200.jpg'
    # url = 'https://i.pximg.net/img-original/img/2021/06/08/16/07/43/90413231_p0.jpg'
