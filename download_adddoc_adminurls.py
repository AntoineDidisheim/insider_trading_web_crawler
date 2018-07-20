import urllib
import pickle
import time
import pandas as pd
import numpy as np

from urllib.error import HTTPError

pd.set_option('display.max_columns', 500)

def cleanS(s):
    s = s.replace('\n','').replace('  ','')
    return s

def mergeLi(temp):
    entry = ""
    for i in range(len(temp)):
        entry = entry + temp[i].split("</li>")[0] + "#"
    return entry

def isNaN(num):
    return num != num


df = pd.read_csv('df_with_civil_url.csv',encoding='utf-8')

df.dtypes.index

# first for the urlCivil
urls = df['urlAdmin']
topLabel = 'adminAddDoc:'

for j in range(0, len(urls)):
    url = urls[j]
    print(j,url)
#problem with 625 manually removed
urls[625] = 'https://research.seed.law.nyu.edu/Search/DocumentDetail/1891/2316/3538'


for j in range(0, len(urls)):
    print(str(j) + "/" + str(len(urls)))
    url = urls[j]
    if not isNaN(url):
        # print(url)
        f = ""
        while f == "":
            try:
                f = urllib.request.urlopen(url).read()
                text_all = str(f)
                text_all = text_all.split('h3less">')
            except HTTPError:
                print(j,'does not load!!!')
                f = "nope"
                text_all = "nope"
            except:
                print("over-ask, wait 60 sec")
                time.sleep(60)
        if len(text_all)>1:
            for t in text_all:
                # t = text_all[1]
                title = t.split("</h3>")[0]
                if title == 'Document Details':
                    ### the top part first
                    temp = t.split('class="col-1-4">\\r\\n ')
                    temp.pop(0)
                    for temp2 in temp:
                        subtitle = temp2.split('\\r\\n')[0]
                        subtitle = topLabel+subtitle.replace(" ","")
                        entry = temp2.split(' <span class="col-3-4 bold">')[1]
                        entry = entry.split('</span>')[0]
                        df.loc[j, subtitle] = entry

                    # now see if there is:
                    temp = t.split('Disgorgement & Penalty Information')
                    if len(temp)>1:
                        resolutions = ""
                        temp = temp[1]
                        temp2 = temp.split('bold headRoom">\\r\\n')
                        for temp3 in temp2:
                            if temp3.split('\\r\\n')[0].replace(" ","") == 'Resolutions':
                                temp4 = temp3.split('span class="col-1-1">\\r\\n ')
                                temp4.pop(0)
                                if len(temp4)>1:
                                    for temp5 in temp4:
                                        resolutions = resolutions+temp5.split("\\r\\n")[0].replace(" ","")+"#"
                                subtitle = topLabel+"resolutions"
                                df.loc[j, subtitle] = resolutions
                            if temp3.split('\\r\\n')[0].replace(" ","") == 'MonetaryPenalties:':
                                temp4 = temp3.split('<h4 class="tightenChildren bold">\\r\\n')
                                for temp5 in temp4:
                                    ### first the individual
                                    subtitle = topLabel+temp5.split('\\r\\n ')[0].replace(" ","")+"Individual"
                                    if len(temp5.split('Individual'))>1:
                                        entry = temp5.split('Individual')[1].split('<span>')[1].split('</span>')[0]
                                        df.loc[j, subtitle] = entry
                                    ### then the shared
                                    subtitle = topLabel+temp5.split('\\r\\n ')[0].replace(" ","")+"Shared"
                                    if len(temp5.split('Shared'))>1:
                                        entry = temp5.split('Shared')[1].split('<span>')[1].split('</span>')[0]
                                        df.loc[j, subtitle] = entry
                    if 'Bars:\\r\\n' in temp:
                        subtitle = topLabel+'bars'
                        temp2 = temp.split('Bars:\\r\\n')[1].split('<li>')
                        temp2.pop(0)
                        entry = ""
                        for temp3 in temp2:
                            entry = entry+temp3.split('</li>')[0]+'#'

                        df.loc[j, subtitle] = entry



df.head()

df.dtypes.index
df = df.drop(['adminAddDoc:Undertakingtomakeapaymentinthenatureofapenaltyintheamountof$50,000totheUnitedStatesTreasuryIndividual',
         'adminAddDoc:Undertakingtomakeapaymentinthenatureofapenaltyintheamountof$50,000totheUnitedStatesTreasuryShared',
              'adminAddDoc:ReimburseOrthofixbonuses,otherincentivebasedorequitybasedcompensationIndividual',
              'adminAddDoc:ReimburseOrthofixbonuses,otherincentivebasedorequitybasedcompensationShared'], axis=1)



df.to_csv('df_with_all_url.csv',encoding='utf-8')
df.shape


df.iloc[625,:]