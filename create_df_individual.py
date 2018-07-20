import urllib
import pickle
import pandas as pd

pd.set_option('display.max_columns', 500)


def cleanS(s):
    s = s.replace('\n','').replace('  ','')
    return s


def mergeLi(temp):
    entry = ""
    for i in range(len(temp)):
        entry = entry + temp[i].split("</li>")[0] + "#"
    return entry

df = pd.DataFrame()
### loop al documents from here 660 44
for j in range(663):
    full_text = open("individual_defenders/"+str(j)+".txt").read()
    # first get defendant names
    title = "Defendant names"
    entry = cleanS(full_text.split('Defendant Name:')[1].split("</span>")[1].split('</h2>')[0])
    df.loc[j, title] = entry

    # split by h3less
    full_text = full_text.split('h3less">')
    ### from here loop all part of full_text on t
    # t = full_text[4]
    # title = t.split("</h3>")[0]
    # title

    for t in full_text:
        # t = full_text[6]
        title = t.split("</h3>")[0]

        if title == 'Initial Case Details':
            # just savign type of case for us latter

            # main course
            temp = t.split('<span class="col-1-4">')
            temp.pop(0)
            for i in range(len(temp)):
                subtitle = cleanS(temp[i].split('</span>')[0])
                entry = cleanS(temp[i].split('<span class="col-3-4 bold">')[1])
                entry = entry.split("</span>")[0]
                df.loc[j,subtitle] = entry
        if title == "Affiliations":
            temp = t.split('<li>')
            temp.pop(0)
            entry = mergeLi(temp)
            df.loc[j,title] = entry

        if title == 'Violations Alleged':
            temp = t.split('<div class="col-1-1 bulletHeader">')
            temp.pop(0)
            for i in range(len(temp)):
                subtitle = cleanS(temp[i].split('</div>')[0])
                temp2 = temp[i].split('<span class="">')
                temp2.pop(0)
                entry = ""
                for ii in range(len(temp2)):
                    entry = entry + cleanS(temp2[ii].split('</span>')[0]) + "#"
                df.loc[j, subtitle] = entry

        if title == 'Other Defendants in Action:':
            temp = t.split('<a href="')
            temp.pop(0)
            entry = ""
            for i in range(len(temp)):
                if '/Search/ActionDetail' in temp[i]:
                    entry = entry + temp[i].split('>')[1].split('<')[0] + '#'
            df.loc[j, title] = entry

        if title == 'Related Violations Alleged':
            temp = t.split('<div class="newRow">')
            temp.pop(0)
            entry = ""
            for i in range(len(temp)):
                if 'ref="/Search/ActionDetail' in temp[i]:
                    entry = cleanS(temp[i].split('<')[0])+\
                            temp[i].split('<')[1].split('>')[1]+\
                            cleanS(temp[i].split('<')[2].split('>')[1])+'#'
                else:
                    entry = cleanS(temp[i]).split('<')[0]+'#'
            df.loc[j, title] = entry

        if title == 'Resolutions':
            temp = t.split('<span class="col-1-3 bold">')

            if 'Bars:\n' in temp[0]:
                subtitle = 'Bars'
                temp2 = temp[0].split('Bars')[1].split('<li>')
                temp2.pop(0)
                entry = mergeLi(temp2)
                df.loc[j, subtitle] = entry

            temp.pop(0)
            for i in range(len(temp)):
                subtitle = cleanS(temp[i].split('</span>')[0])
                temp2 = temp[i].split('<span class="col-2-3">')
                temp2.pop(0)
                entry = cleanS(temp2[0].split('</span>')[0])
                df.loc[j, subtitle] = entry

        if title == 'Related Documents:':
            if df['Initial Filing Format'][j] == 'Civil Proceeding':
                subtitle = 'urlCivil'
                temp = t.split("href")
                temp3 = "no_found"
                for temp2 in temp:
                    if "final" in temp2.lower() and "judgment" in temp2.lower():
                        temp3 = temp2.split('"')
                if not temp3=="no_found":
                    temp3 = temp3[1]
                    url = 'https://research.seed.law.nyu.edu'+temp3
                    # f = urllib.request.urlretrieve(url)
                    df.loc[j, subtitle] = url
            if df['Initial Filing Format'][j] == 'Administrative Action':
                subtitle = 'urlAdmin'
                temp = t.split("href")
                temp3 = "not"
                for temp2 in temp:
                    if "administrative" in temp2.lower() and "proceeding" in temp2.lower():
                        if temp3 == "not":
                            temp3 = temp2.split('"')

                temp3 = temp3[1]
                url = 'https://research.seed.law.nyu.edu' + temp3
                # f = urllib.request.urlretrieve(url)
                df.loc[j, subtitle] = url





df.head()
df.to_csv('df.csv',encoding='utf-8')
df.shape
## related documents ? Related Violations Alleged ? Related Documents: ? Other Defendants in Action:? Related action ?
