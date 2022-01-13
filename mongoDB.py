import pymongo
from pymongo import Mongoclient

cluster = Mongoclient(mongodb+srv://yashwardhan:PY74NORNY5OnUrH6@cluster0.1wicn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority)
db = cluster["rooms"]