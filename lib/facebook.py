import re
import asyncio
import requests
from bs4 import BeautifulSoup as parser


class User(object):
    def __init__(self, *data, **kwargs):
        for i in data:
            for dictionary in i:
                for key in dictionary:
                    setattr(self, key, dictionary[key])
            for key in kwargs:
                setattr(self, key, kwargs[key])

class Facebook:

    def __init__(self):
        self.users = []
        self.__cookie = None
        self.__ses = requests.Session()
        self.url = "https://mbasic.facebook.com"
    
    @property
    def cookie(self):
        return self.__cookie

    @property
    def validate(self):
        c = {}
        r = parser(self.__ses.get(self.url,cookies=self.__cookie).text,"html.parser")
        if "mbasic_logout_button" in str(r):
            for i in self.__cookie['cookie'].split(';'):
                key,value = i.replace(' ','').split('=')
                c[key] = value
            
            self.__ses.cookies.update(c)

            return True
        
        return False
    

    @cookie.setter
    def set_cookie(self,cookie):
        self.__cookie = {"cookie":cookie}


    async def getdatachat(self,data):
        name = re.findall('<strong\sclass\=\".*\">(.*?)<\/strong>',data)[0],
        body = re.findall('<div><span>(.*?)<\/span><div',data)
        url  = re.findall('\saction\=\"(\/messages\/send\/.*?)\"\sclass',data)[0]
        return name[0],body[len(body)-1],url


    async def get_chats(self):
        chat = []
        m = self.__ses.get(self.url).text
        msg = re.findall('<\/a><a\shref\=\"(\/messages\/.*?)\"',m)
        for i in msg:
            chat.append(i)
        
        return chat
    

    async def get_message(self):
        msg = await self.get_chats()
        if len(msg) != 0:
            for i in msg:
                r = self.__ses.get(self.url + i).text
                d = parser(r,"html.parser").find_all("input",{"type":"hidden"})
                x = await self.getdatachat(r)
                self.users.append({"name":x[0],"body":x[1],"url_chat":i,"to":x[2],"data":{
                    "fb_dtsg":d[3]['value'],
                    "jazoest":d[4]['value'],
                    "send":"Send",
                    "tids":d[5]['value'],
                    "wwwup":d[6]['value'],
                    f"ids[{d[7]['value']}]":d[7]['value'],
                    "platform_xmd":"",
                    "referrer":"",
                    "ctype":"",
                    "cver":d[11]['value'],
                    "csid":d[12]['value']
                }})
        
            return User(self.users)
        
        return None


    async def send_message(self,to,data,message):
        data.update({'body':message})
        return self.__ses.post(self.url + to,data=dict(data))

