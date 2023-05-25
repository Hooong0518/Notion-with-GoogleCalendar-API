# 必要套件、參數設定
from notion_client import Client
import datetime
import json
notion = Client(auth = 'secret_fOpZe1XOU5ZsKjONC6pvrA5TVwEG5UFgV2aSHAJft6T') # Intagration Secret
DATABASE_ID = '8d18ec8d0c0c40ff819d5b175c81bdbe' # Database ID

with open("json/filter.json", "r", encoding = 'utf-8') as f:
    FILTER = json.load(f)
    FILTER["update"]["and"][2]["last_edited_time"]["on_or_after"] = datetime.date.today().isoformat()
#取得資料庫資料
def query_insertData():
    results = [] # 存放結果
    next_cursor = None # 存放頡取資料的開始位置
    while True:
        query_params = {
            "database_id": DATABASE_ID,
            "page_size": 100,
            "start_cursor": next_cursor,
            "filter": FILTER['insert'],
        }
        res = notion.databases.query(**query_params)
        results += res["results"]
        next_cursor = res.get('next_cursor') # 更新開始位置
        if not next_cursor: break
    return results
def query_updateData():
    results = [] # 存放結果
    next_cursor = None # 存放頡取資料的開始位置
    while True:
        query_params = {
            "database_id": DATABASE_ID,
            "page_size": 100,
            "start_cursor": next_cursor,
            "filter": FILTER['update'],
        }
        res = notion.databases.query(**query_params)
        results += res["results"]
        next_cursor = res.get('next_cursor') # 更新開始位置
        if not next_cursor: break
    return results
def query_deleteData():
    results = [] # 存放結果
    next_cursor = None # 存放頡取資料的開始位置
    while True:
        query_params = {
            "database_id": DATABASE_ID,
            "page_size": 100,
            "start_cursor": next_cursor,
            "filter": FILTER['delete'],
        }
        res = notion.databases.query(**query_params)
        results += res["results"]
        next_cursor = res.get('next_cursor') # 更新開始位置
        if not next_cursor: break
    return results
query_deleteData()
# 新增頁面
def new_page(page):
    res = notion.pages.create(parent={"database_id": DATABASE_ID}, properties=page)
    return res
# 更新頁面
def update_page(page_id, properties):
    res = notion.pages.update(page_id = page_id, properties=properties)
    return res
# 刪除頁面
def delete_page(page_id):
    res = notion.pages.delete(page_id)
    return res