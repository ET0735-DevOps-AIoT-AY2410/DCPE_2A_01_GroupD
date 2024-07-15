import requests
import os
import json

# Reference for endpoints https://www.mongodb.com/docs/atlas/app-services/data-api/examples/
# https://www.mongodb.com/docs/manual/reference/operator/update/
# Developed from scratch, entirely by Leroy-Hong

class MongoDB:
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-pjyjw/endpoint/data/v1/action/"
    headers = {"Content-Type": "application/ejson", 
            "Accept": "application/json",
            "apiKey": os.environ["APIKEY"]}

    data : dict

    def getItems(self, filter = None):
        temp = self.data.copy()
        temp["filter"] = filter
        response = requests.post(url=self.url+"find", headers=self.headers, json=temp)
        responseD = response.content.decode('ASCII')
        return json.loads(responseD)["documents"]
    
    def listItems(self):
        print(self.getItems())    

    def insertItem(self, doc):
        temp = self.data.copy()
        temp["document"] = doc
        response = requests.post(url=self.url+"insertOne", headers=self.headers, json=temp)
        return response.content
    
    def updateItem(self, search, doc):
        temp = self.data.copy()
        temp["filter"] = search
        temp["update"] = {
            "$set": doc
        }
        response = requests.post(url=self.url+"updateOne", headers=self.headers, json=temp)
        return response.content

    def appendItem(self, search, doc):
        temp = self.data.copy()
        temp["filter"] = search
        temp["update"] = {
            "$addToSet": doc
        }
        response = requests.post(url=self.url+"updateOne", headers=self.headers, json=temp)
        return response.content

    def __init__(self, collection = "Testing") -> None:
        self.data = {
        "dataSource": "SPDevOpsLibrary",
        "database": "Library",
        "collection": collection}

if __name__ == "__main__":
    db = MongoDB('books')
    # print(db.insertItem(doc= {"time":"2:11AM wallahi im finished"}))
    # print(db.updateItem(search= {"borrowedBooks"}))
    db.listItems()