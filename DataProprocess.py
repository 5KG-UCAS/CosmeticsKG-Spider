import pandas as pd
import re
class DataProprocesser():
    def __init__(self,categorys=['kouhong','fendiye','meibi','saihong','sanfen','xiangshui','zhexia','yanying']):
        self.data_dir = './data/'
        self.categorys = categorys
        self.data = {}
        for cate in categorys:
            self.data[cate] = pd.read_csv(self.data_dir + cate + '_data.csv')

    def get_brand(self):
        brands = pd.DataFrame()
        for cate in self.categorys:
            df_temp = self.data[cate]['goods_name'].str.split('/',expand=True)
            brand = pd.DataFrame()
            brand['eng'] = df_temp[0].drop_duplicates()
            brand['chi'] = df_temp[1].str.split(' ',expand=True)[0].drop_duplicates()
            brands = brands.append(brand)
        brands.to_csv(self.data_dir+'brands.csv')

    def wash_xiangshui(self):
        data = self.data['xiangshui']
        # VERSACE/范思哲 晶钻女士（粉钻）香水 50ml
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+) (?P<Name>.+)[ /](?P<size>\d+)[ml,ML]?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        data = pd.concat([data,df_new], axis=1)
        data.to_csv(self.data_dir+'xiangshui_data.csv',index =False)

    def wash_meibi(self):
        data = self.data['meibi']
        # shu uemura/植村秀 经典砍刀眉笔
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+) (?P<Name>.+)'
        df_new = data['goods_name'].str.extract(patt, expand=True)
        data = pd.concat([data, df_new], axis=1)
        print(data)
        data.to_csv(self.data_dir + 'meibi_data.csv', index=False)
    # TODO:wash data-----start-----珂珂小仙女
    def wash_sanfen(self):
        # ready
        data = self.data['sanfen']
        patt = r'^(?P<engName>.*)/(?P<chiName>[ ]?[^ ]+)?(?P<Name>.+?\D+)(?P<size>\d+[g])?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        data = pd.concat([data,df_new], axis=1)
#        data.to_csv(self.data_dir+'sanfen_data.csv',index =False)
        data.to_csv(self.data_dir+'sanfen_test.csv',index =False)   
        print(data)       
        return None

    def wash_zhexia(self):
        data = self.data['zhexia']
        patt = r'^(?P<engName>.*)[\s](?P<Name>.+?\D+)(?P<size>\d+)?[g,ml]?'
        df_new = data['goods_name'].str.extract(patt,expand=True)
        data = pd.concat([data,df_new], axis=1)
#        data.to_csv(self.data_dir+'sanfen_data.csv',index =False)
        data.to_csv(self.data_dir+'zhexia_test.csv',index =False)   
        print(data)  

    def wash_fendiye(self):      
        data = self.data['fendiye']        
        patt1 = r'^(?P<engName>.*\D+)[/](?P<chiName>[ ]?[^ ]+) (?P<Name1>[^ ]+)(?P<color>.*)?'
        df_new = data['goods_name'].str.extract(patt1,expand=True)  
        data = pd.concat([data,df_new], axis=1)
        data.to_csv(self.data_dir+'fendiye_data.csv',index =False)                 
        data = self.data['fendiye']         
        patt2 = r'^(?P<Name>\D+)(?P<size>\d+)?[g,ml]+?'
        df_new = data['Name1'].str.extract(patt2,expand=True)   
        data = pd.concat([data,df_new], axis=1)
#        data.to_csv(self.data_dir+'sanfen_data.csv',index =False)
        data.to_csv(self.data_dir+'fendiye_test.csv',index =False)   
        print(data)  
#
#    def wash_saihong(self):
#        return None
#
#    def wash_yanying(self):
#        # 先不弄
#        return None
#
#    def wash_kouhong(self):
#        return None

    # TODO:wash data-----end-----珂珂小仙女

dp = DataProprocesser()
#dp.wash_meibi()
# brand = dp.data['xiangshui'][['engName','chiName']]
# brand = brand.drop_duplicates()
# brand.to_csv(dp.data_dir+'brand.csv',index = False)
