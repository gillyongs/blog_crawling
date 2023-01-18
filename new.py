import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import os
import re

def clean_text(inputString):
    text_rmv = re.sub('[\\\/:*?"<>|]', ' ', inputString)
    text_rmv = text_rmv.strip()
    return text_rmv


#id = 'khs20010327'
#category = '592'

id = 'noh0058'
category = '132'
start = 99
number = 100

end = int(number/5 + start)
dir = "C:/Users/user/Desktop/Naverblog"
os.chdir(dir)
linklist=[]
for i in range (start, end):
    category_url = "https://blog.naver.com/PostTitleListAsync.naver?blogId="+id+"&viewdate=&currentPage="+str(i)+"&parentCategoryNo="+category+"&countPerPage=5"
    categoryresponse = requests.get(category_url)
    categorytext = categoryresponse.text
    categorysoup = categorytext.split('"tagQueryString":"')[1].replace('"}', '')
    logNo = categorysoup.split("&logNo=")
    logNo.remove("")
    for i2 in logNo:
        link = "https://m.blog.naver.com/"+id+"/"+i2
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('meta', property="og:title")['content']
        file_box = soup.find('div', id='_photo_view_property')
        file = file_box['attachimagepathandidinfo'].strip("[""]").replace('"path"', '').replace('"id"', '').split('"')
        save_path = "./"+clean_text(title)+"/"
        if not os.path.exists("./"+clean_text(title)):
            os.makedirs("./"+clean_text(title))
        for i in range(0, 9999):
            k = i*2 + 1
            try:
                filelink = "https://blogfiles.pstatic.net" +file[k]
            except:
                print("완료\n")
                break
            urllib.request.urlretrieve(filelink, save_path+clean_text(urllib.parse.unquote(filelink.split('/')[-1])))
        

