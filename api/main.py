from typing import Union
from fastapi import FastAPI
import re
from snscrape.modules.twitter import TwitterUserScraper

app = FastAPI()

@app.get("/")
def hello():
    return {"Hello User!, This API is used to convert" : "Twitter ID to USERNAME and vice versa"}

@app.get("/twc/")
async def read_item(val):
    res = bool(re.search(r"\s", val))
    if not res:
        try:
            val = int(val)
        except:
            val = val.replace("@","")
        
        # fetching username as val is numerical id
        if type(val)==int:
            try:
                Screen_Name = TwitterUserScraper(val).entity.username
                response = '200'
            except AttributeError:
                Screen_Name = f"USER ID - {val} DOES NOT EXIST, kindly enter correct userID"
                response = '404'
        # fetching ID as val is username
        else:
            try:
                User_ID = TwitterUserScraper(val).entity.id
                response = '200'
            except AttributeError:
                User_ID = f"USERNAME - @{val} DOES NOT EXIST, kindly enter correct username"
                response = '404'
    
        if type(val)==int: return {'response':response,'data': '@'+Screen_Name}
        else: return {'response':response,'data': User_ID}   
            
    # handling incrrect username format i.e it contains spaces 
    else:return {'response':'404','data':f"INCORRECT USERNAME FORMAT - {val} contains spaces, kindly enter correct username"}
    