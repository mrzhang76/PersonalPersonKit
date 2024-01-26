import json 
from urllib.parse import urlparse
from urllib.parse import parse_qs
from pixivpy3 import *
class PixivContentProcess():
    def PixivNovelJsonProcess(self,novel_detail,novel_text):#处理文章JSON
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
    
    def PixivNovelDownload(self,novellist,api): #按列表下载文章
        for novelid in novellist.keys():
            novel_detail = api.novel_detail(novelid)
            novel_text = api.novel_text(novelid)
            self.PixivNovelJsonProcess(novel_detail,novel_text)

    def GetPixivNovelMarkedList(self,Userid,api): #获取用户收藏文章列表 
        result = self.PixivNovelMarkedProcess(Userid,api)
        novels = result['novels']
        max_bookmark_id = result['new_max_bookmark_id']
        while(max_bookmark_id!=''):
            result = self.PixivNovelMarkedProcess(Userid,api,_max_bookmark_id=max_bookmark_id)
            novels = novels + result['novels']
            max_bookmark_id = result['new_max_bookmark_id']
        novels = self.PixivNovelMarkedListProcess(Userid,novels)
        return novels

    def PixivNovelMarkedProcess(self,Userid,api,_max_bookmark_id:int |str = None): #文章收藏翻页
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
    
    def PixivNovelMarkedListProcess(self,Userid,novels): #处理收藏文章列表
        processed_novels = {}
        for novel in novels:
            processed_novels[str(novel['id'])] = novel['title']
        with open('User'+str(Userid) + ".json", "w",encoding="utf8") as write_file:
             json.dump(processed_novels,write_file,ensure_ascii=False,indent=4)
        return processed_novels
    
    def GetPixivNovelbySeries(self,series_id,api): #按系列返回文章列表
        series = {'series_detail':'','series_novel':''}
        result = self.PixivNovelSeriesProcess(series_id,api)
        series['series_detail'] = (result['series'])["series_detail"]
        series_novel = (result['series'])["series_novel"]
        last_order = result['new_last_order']
        while(last_order!=''):
            result = self.PixivNovelSeriesProcess(series_id,api,last_order)
            series_novel.update((result['series'])["series_novel"])
            last_order = result['new_last_order']
        series['series_novel'] = series_novel 
        return series
    
    def PixivNovelSeriesProcess(self,series_id,api,last_order: str | None = None): #按系列获取文章列表
        result = {'series':'','new_last_order':''}
        if(last_order!=None):
            json_result = api.novel_series(series_id,last_order=last_order)
        else:
            json_result = api.novel_series(series_id)
        result['series'] = self.PixivNovelSeriesJsonProcess(json_result)
        print(json_result["next_url"])
        if(json_result["next_url"]!=None):
            result['new_last_order'] = ((parse_qs(urlparse(json_result["next_url"]).query))['last_order'])[0]
            print(result['new_last_order'])
        else: 
            result['new_last_order'] = ''
        return result
    
    def PixivNovelSeriesJsonProcess(self,novel_series): #处理系列文章返回JSON
        series_novel = {}
        for novel in novel_series["novels"]:
                series_novel[str(novel["id"])] = novel["title"]
        series_detail = {"series_id":(novel_series["novel_series_detail"])["id"],
                 "series_title":(novel_series["novel_series_detail"])["title"],
                 "author_id":((novel_series["novel_series_detail"])["user"])["id"],
                 "author_name":((novel_series["novel_series_detail"])["user"])["name"],
                 "caption":(novel_series["novel_series_detail"])["caption"],
                 }
        series = {"series_detail":series_detail,
                  "series_novel":series_novel
                 }
        return series