import pandas as pd
import numpy as np
import re
class DataProprocesser():
    '''
                list    detail  wash    import
        粉底液    √       √
        口红      √       √
        眉笔      √       √       √
        腮红      √       √
        散粉      √       √
        香水      √       √       √
        眼影      √       先不弄
        遮瑕      √       √
    '''
    def __init__(self,categorys=['kouhong','fendiye','meibi','saihong','sanfen','xiangshui','zhexia','yanying']):
        self.data_dir = './data/'
        self.washed_dir = './data_washed/'
        self.categorys = categorys
        self.data = {}
        for cate in categorys:
            self.data[cate] = pd.read_csv(self.data_dir + cate + '_data.csv')


    def get_brand(self):
        brands = pd.DataFrame()
        for cate in self.categorys:
            data = pd.read_csv(self.washed_dir+cate+'_data.csv')
            if data.keys().contains('engName'):
                brand = pd.DataFrame()
                brand['eng'] = data['engName']
                brand['chi'] = data['chiName']
                brands = brands.append(brand)
        brands = brands.drop_duplicates()
        brands.to_csv(self.data_dir+'brands.csv', index=False)

    def delete_dirty(self):
        for cate in self.categorys:
            data = self.data[cate]

            data = data[~data["goods_name"].str.contains("套装")]
            data = data[~data["goods_name"].str.contains("支装")]
            data.loc[:,'goods_name']= data['goods_name'].str.replace('热卖','')
            data.loc[:, 'goods_name'] = data['goods_name'].str.replace('（hot）', '')
            data.to_csv(self.data_dir+ cate + '_data.csv', index=False)

    def wash_xiangshui(self):
        data = self.data['xiangshui']
        # VERSACE/范思哲 晶钻女士（粉钻）香水 50ml
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+) (?P<Name>.+)[ /](?P<size>\d+)[ml,ML]?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        data = pd.concat([data,df_new], axis=1)
        data = data.set_index()
        data.to_csv(self.washed_dir+'xiangshui_data.csv',index =False)

    def wash_meibi(self):
        data = self.data['meibi']
        # shu uemura/植村秀 经典砍刀眉笔 #02/灰棕色
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+) (?P<Name>.+) #(?P<Code>\d+)?/?(?P<Color>.+)?'
        data = data.drop(['engName', 'chiName', 'Name' ,'Code','Color'],axis=1)
        df_new = data['goods_name'].str.extract(patt, expand=True)
        print(df_new)
        data = pd.concat([data, df_new], axis=1)
        data.to_csv(self.washed_dir + 'meibi_data.csv', index=False)
    # TODO:wash data-----start-----珂珂小仙女
    def wash_sanfen(self):
        # ready
        data = self.data['sanfen']
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+)?(?P<Name>.+?\D+)(?P<size>\d+[g])?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        print(df_new)
        data = pd.concat([data,df_new], axis=1)
        data = data.loc[data['chiName'].notna()]
        # data.to_csv(self.washed_dir+'sanfen_data.csv',index =False)
        return None

    def wash_zhexia(self):
        data = self.data['zhexia']
        patt = r'^(?P<engName>.*)[\s](?P<Name>.+?\D+)(?P<size>\d+)?[g,ml]?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        data = pd.concat([data,df_new], axis=1)
#        data.to_csv(self.data_dir+'sanfen_data.csv',index =False)
        data.to_csv(self.washed_dir+'zhexia_test.csv',index =False)

    def wash_fendiye(self):      
        data = self.data['fendiye']        
        patt1 = r'^(?P<engName>.*\D+)[/](?P<chiName>[ ]?[^ ]+) (?P<Name1>[^ ]+)(?P<color>.*)?'
        df_new = data['goods_name'].str.extract(patt1,expand=True)  
        data = pd.concat([data,df_new], axis=1)
        data.to_csv(self.washed_dir+'fendiye_data.csv',index =False)
        data = self.data['fendiye']         
        patt2 = r'^(?P<Name>\D+)(?P<size>\d+)?[g,ml]+?'
        df_new = data['Name1'].str.extract(patt2,expand=True)   
        data = pd.concat([data,df_new], axis=1)
#        data.to_csv(self.data_dir+'sanfen_data.csv',index =False)
        data.to_csv(self.washed_dir+'fendiye_test.csv',index =False)

   # def wash_saihong(self):
   #     return None
   #
    # TODO:wash data-----end-----珂珂小仙女
    def wash_kouhong(self):
        data = self.data['kouhong']
        data = data[~data["goods_name"].str.contains(r"\*")] #洗掉套装
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('N°', '#')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace(r'N\d', '#')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('雅诗兰黛', 'Estee Lauder/雅诗兰黛')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('NARS', 'NARS/NARS')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('3CE', '3CE/3CE')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('CHARLOTTE  TILBURY', 'CHARLOTTE  TILBURY/夏洛特·蒂尔伯里')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('Hourglass', 'Hourglass/沙漏')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('KIKO', 'KIKO/奇寇')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('露华浓', 'Revlon/露华浓')
        data.loc[:, 'goods_name'] = data['goods_name'].str.replace('PAT McGRATH', 'PAT McGRATH/彩妆大师')
        patt = r'^(?P<engName>[^\u4E00-\u9FA5]*)/(?P<chiName>[ ]?[^ ]+) (?P<name>[^ ]+) (?P<Other>.+)'
        df_new = data['goods_name'].str.extract(patt, expand=True)
        df_new.loc[:,'name'] = df_new['name'].str.replace(r'[\dg\.ml]','') # 洗掉规格
        print(df_new)
        print(len(df_new.loc[df_new['name'].notna()]) / len(df_new))
        # 开始洗尾巴
        patt2 = r'(?P<code>#.*\d+)?(?P<sub_name>.+)?'
        df_new_new = df_new['Other'].str.extract(patt2, expand=True)
        df_new_new.loc[:, 'code'] = df_new_new['code'].str.replace(r'[^\d]+', '') #洗掉非数字
        df_new_new.loc[:, 'sub_name'] = df_new_new['sub_name'].str.replace(r'[^A-za-z\u4E00-\u9FA5 ]+', '') #洗掉非中英文字符或空格
        print(df_new_new)
        print(df_new.iloc[df_new_new.loc[~df_new_new['sub_name'].notna() & ~df_new_new['code'].notna()].index.tolist()])
        print(1-len(df_new_new.loc[~df_new_new['sub_name'].notna() & ~df_new_new['code'].notna()])/len(df_new_new))
        data['engName'] = df_new['engName']
        data['chiName'] = df_new['chiName']
        data['name'] = df_new['name']
        data['code'] = df_new_new['code']
        data['sub_name'] = df_new_new['sub_name']
        print(data)
        data = data.drop(['href','xinxin_price','bid_price_min'] ,axis=1)
        data.to_csv(self.washed_dir + 'kouhong_data.csv', index=False)


dp = DataProprocesser()
# dp.wash_xiangshui()
# dp.delete_dirty()
dp.data['xaingshui']


# [Hourglass', 'CHARLOTTE']