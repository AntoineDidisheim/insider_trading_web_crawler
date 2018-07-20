import urllib
import pickle

########### loading and saving all the html files
url_list = pickle.load(open("individual_url.p", "rb"))

url = url_list[1]
for i in range(601,len(url_list)):
    url = url_list[i]
    f = urllib.request.urlretrieve(url, "individual_defenders/"+str(i)+".txt")
    print(str(i)+"/"+str(len(url_list)))
# print(f.read())
# f.response()