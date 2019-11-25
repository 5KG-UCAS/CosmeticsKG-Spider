import requests
import sys
import io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
class mySpider():

    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) network/wifi xinxin/1.9.15 iPhone11,8 sc(3560f81c0c81f8b4e9cdfb96c3da0db9ffd39ef0,appstore) Mobile',
                       'Accept-Language': 'zh-Hans-CN;q=1',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Connection': 'keep-alive'
        }
        self.host = "https://api.xinxinapp.cn"
        self.paras = {'clientCode': 'E76AF9B6-0CE9-407B-AB56-AC5E517EBDB5',
                      'platform': 'ios',
                      'v': '1.9.15'
                      }

    def get_json(self,router,get_paras:dict):
        get_paras.update(self.paras)
        print("request ",router)
        rsp = requests.get(self.host+router, params=get_paras, headers=self.header)
        return rsp.json()

    def get_list(self, page):
        list_router = '/goods/get.goods.list/v1'
        router_paras ={'timestamp': '1574679000',
                       'token': '1f12b470a6720db468a1d181c3404204',
                       'cat_id': 1,
                       'page': page,
                       'page_size': 20,
                       'version': '101'}
        rsl = self.get_json(list_router, get_paras=router_paras)
        print(rsl.url)
        list = rsl['data']['list']
        return list

    def get_detail(self,id,goods_id):
        detail_router = '/goods/get.goods.detail/v1'
        router_paras={'timestamp': '1574679000',
                      'token': 'c730213566969d4a8bd7ebd6486a5f36',
                      'flag': 2,
                      'goods_id': goods_id,
                      'id': id,
                      'route': 'goodsDetail',
                      'version': '105'
        }
        rsl = self.get_json(detail_router, get_paras=router_paras)
        print(rsl)
        return None

    def run(self):
        page = 1
        # TODO finish condition
        # TODO other type
        print("start...")
        print("getting list in page ",page)
        list = self.get_list(page)
        for item in list:
            id = item['id']
            goods_id = item['goods_id']
            # TODO is this goods has save?
            if(False):
                print('has get')
            else:
                self.get_detail(id,goods_id)

print("123")
spider = mySpider()

spider.run()

