import pickle
########### First loading all url to look for
firstPage = open("firstPage.txt").read()

firstPage = firstPage.split("href")

firstPage = [x.split('"') for x in firstPage]
firstPage = [x[1] for x in firstPage]
firstPage
# [item.upper() for item in mylis]

key = "/Search/ActionDetail"

temp = []
for t in firstPage:
    if key not in t:
        temp.append(t)
firstPage = [x for x in firstPage if x not in temp]

firstPage = ['https://research.seed.law.nyu.edu'+x for x in firstPage]

pickle.dump(firstPage, open("individual_url.p", "wb"))
del temp, key, t