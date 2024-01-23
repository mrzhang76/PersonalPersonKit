import json 
from urllib.parse import urlparse
from urllib.parse import parse_qs
from pixivpy3 import *
class PixivContentProcess():
    def PixivNovelJsonProcess(self,novel_detail,novel_text):
        novel = {"novel_id":(novel_detail["novel"])["id"],
                 "novel_title":(novel_detail["novel"])["title"],
                 "series_id":((novel_detail["novel"])["series"])["id"],
                 "series_title":((novel_detail["novel"])["series"])["title"],
                 "author":((novel_detail["novel"])["user"])["name"],
                 "author_id":((novel_detail["novel"])["user"])["id"],
                 "novel_content":novel_text["novel_text"]
                 }
        with open("./novels/"+novel["novel_title"]+".json", "w",encoding="utf8") as write_file:
              json.dump(novel,write_file,ensure_ascii=False)
        return novel
    
    def PixivNovelDownload(self,novellist,api):
        for novelid in novellist.keys():
            novel_detail = api.novel_detail(novelid)
            novel_text = api.novel_text(novelid)
            self.PixivNovelJsonProcess(novel_detail,novel_text)

    def GetPixivNovelMarkedList(self,Userid,api):
        result = self.PixivNovelMarkedProcess(Userid,api)
        novels = result['novels']
        max_bookmark_id = result['new_max_bookmark_id']
        while(max_bookmark_id!=''):
            result = self.PixivNovelMarkedProcess(Userid,api,_max_bookmark_id=max_bookmark_id)
            novels = novels + result['novels']
            max_bookmark_id = result['new_max_bookmark_id']
        novels = self.PixivPixivNovelMarkedListProcess(Userid,novels)
        return novels

    def PixivNovelMarkedProcess(self,Userid,api,_max_bookmark_id:int |str = None):
        result = {'novels':'','new_max_bookmark_id':''}
        if(_max_bookmark_id!=''):
            json_result = api.user_bookmarks_novel(Userid,max_bookmark_id=_max_bookmark_id)
        else:
            json_result = api.user_bookmarks_novel(Userid)
        result['novels'] = json_result["novels"]
        if(json_result["next_url"]!=None):
            result['new_max_bookmark_id'] = ((parse_qs(urlparse(json_result["next_url"]).query))["max_bookmark_id"])[0]
        else: 
            result['new_max_bookmark_id'] = ''
        return result
    
    def PixivPixivNovelMarkedListProcess(self,Userid,novels):
        processed_novels = {}
        for novel in novels:
            processed_novels[str(novel['id'])] = novel['title']
        with open('User'+str(Userid) + ".json", "w",encoding="utf8") as write_file:
             json.dump(processed_novels,write_file,ensure_ascii=False,indent=4)
        return processed_novels