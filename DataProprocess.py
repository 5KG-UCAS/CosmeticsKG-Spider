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



dp = DataProprocesser()
# dp.wash_xiangshui(
an = dp.data['xiangshui']['goods_name'].to_list()
reg = re.compile('^(?P<engName>.*)/(?P<chiName>.+) (?P<Name>.+) (?P<size>\d+ml)$')
num = 0
for str in an:
    regMatch = reg.match(str)

    if regMatch:
        print(regMatch.groupdict())
        num += 1
    else:
        print('Error in '+str)

print(num/len(an))
