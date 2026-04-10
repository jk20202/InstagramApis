import uvicorn
from apis.ins_apis import INS_Apis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

apis = INS_Apis()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
    获取WorkDocID
    :json url: 文章的url
    :json cookies_str: cookies
    返回comment的docid1和docid2
"""
@app.post("/get_WorkCommentDocID")
def get_WorkCommentDocID(data: dict):
    try:
        url = data["url"]
        cookies_str = data["cookies_str"]
        success, msg, res = apis.get_WorkCommentDocID(url, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取XIgAppId和主页的docid
    :json username: 用户名
    :json cookies_str: cookies
"""
@app.post("/get_info")
def get_info(data: dict):
    try:
        username = data["username"]
        success, msg, res = apis.get_info(username)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取用户的信息
    :json username: 用户名
    :json XIgAppId: XIgAppId
    :json cookies_str: cookies
"""
@app.post("/get_user_info")
def get_user_info(data: dict):
    try:
        username = data["username"]
        XIgAppId = data["XIgAppId"]
        cookies_str = data["cookies_str"]
        success, msg, res = apis.get_user_info(username, XIgAppId, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取用户的所有作品
    :json user_id: 用户id
    :json DocID: 主页的docid
    :json cookies_str: cookies
"""
@app.post("/get_user_all_videos")
def get_user_all_videos(data: dict):
    try:
        user_id = data["user_id"]
        DocID = data["DocID"]
        cookies_str = data["cookies_str"]
        success, msg, res = apis.get_user_all_videos(user_id, DocID, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取用户所有评论
    :json CommentDocID: 作品的一级和二级评论的docid
    :json mediaID: 作品的mediaID
    :json cookies_str: cookies
"""
@app.post("/get_work_all_comments")
def get_work_all_comments(data: dict):
    try:
        CommentDocID = data["CommentDocID"]
        mediaID = data["mediaID"]
        cookies_str = data["cookies_str"]
        success, msg, res = apis.get_work_all_comments(CommentDocID, mediaID, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取一篇ins的详细信息
    :json url: 文章的url
    :json cookies_str: cookies
"""
@app.post("/get_inswork_info")
def get_inswork_info(data: dict):
    try:
        url = data["url"]
        cookies_str = data["cookies_str"]
        success, msg, res = apis.get_inswork_info(url, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5005, forwarded_allow_ips='*')
