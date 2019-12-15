import requests
import sys
import io
import os
from tqdm import tqdm
import time
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
class mySpider():

    def __init__(self,categorys=['kouhong','fendiye','meibi','saihong','sanfen','xiangshui','zhexia','yanying']):
        self.url_dir = './url/'
        self.data_dir = './data/'
        # self.categorys=['kouhong']
        self.categorys=categorys
        self.header = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) network/wifi xinxin/1.9.15 iPhone11,8 sc(3560f81c0c81f8b4e9cdfb96c3da0db9ffd39ef0,appstore) Mobile',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
            }

        # parse goodslist url
        self.goodslist_url = {}
        for label in self.categorys:
            self.goodslist_url[label]=[]
            f = open(self.url_dir+'goodslist_'+label+'.txt','r',encoding='utf-16')
            try:
                for line in f.readlines():
                    if line != '\n':
                        self.goodslist_url[label].append(line)
            finally:
                f.close()

        #parse goodsdetail url
        self.goodsdetail_url = {}
        for label in self.categorys:
            self.goodsdetail_url[label] = []
            if not os.path.exists(self.url_dir + 'detail_' + label + '.txt'):
                continue
            f = open(self.url_dir + 'detail_' + label + '.txt', 'r', encoding='utf-16')
            try:
                for line in f.readlines():
                    if line != '\n' and line.find('detail')>=0:
                        self.goodsdetail_url[label].append(line)
            finally:
                f.close()


    def get_json(self,url):
        rsp = requests.get(url=url, headers=self.header)
        return rsp.json()

    def get_list(self, categorys = []):
        if len(categorys) == 0:
            categorys = self.categorys
        for label in categorys:
            filename = './'+label+'_data.csv'
            if os.path.exists(self.data_dir+filename):
                df = pd.read_csv(self.data_dir+filename)
            else:
                df = pd.DataFrame()
            urls = tqdm(self.goodslist_url[label])
            urls.set_description("Processing %s" % label)
            for url in urls:
                rsl = self.get_json(url)
                goods_list = rsl['data']['list']
                for goods in goods_list:
                    df = df.append(goods, ignore_index=True)
            df = df.drop_duplicates(['id'])
            df.to_csv(self.data_dir+filename, index=False)


    def get_detail(self, categorys = []):
        if len(categorys)==0:
            categorys = self.categorys
        for label in categorys:
            filename = './' + label + '_data.csv'
            if os.path.exists(self.data_dir+filename):
                df = pd.read_csv(self.data_dir+filename)
            else:
                continue

            urls = tqdm(self.goodsdetail_url[label])
            urls.set_description("Processing %s" % label)
            for url in urls:
                rsl = self.get_json(url)
                goods_detail_list = rsl['data']['goods_attr']
                for goods in goods_detail_list:
                    id = goods['id']
                    for attr in ['attr_name', 'example_img', 'counter_price', 'xinxin_price', 'bid_price_min']:
                        df.loc[df['id'] == id,attr] = goods[attr]


            df.to_csv(self.data_dir + filename, index=False)

        return None


spider = mySpider()

spider.get_list()
spider.get_detail(categorys=['kouhong','fendiye','meibi','saihong','sanfen','zhexia',])
