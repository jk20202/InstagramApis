import json
import re
import requests

from utils.ins_utils import get_common_headers, get_requests_userinfo_headers, trans_cookies_str_to_dict


class INS_Apis():

    """
        辅助函数 获取HomeDocID
        获取DocID
        :param res_text: 主页html
        返回DocID
    """
    def get_HomeProfileDocID(self, res_text: str):
        success = True
        msg = '成功'
        DocID = None
        try:
            scripts_url = re.findall(r'<script src="(.*?)"', res_text)
            scripts_url = [url for url in scripts_url if url.startswith("http")]
            headers = get_common_headers()
            for url in scripts_url:
                response = requests.get(url, headers=headers)
                res = response.text
                DocID = re.findall(r'__d\("PolarisProfilePostsActions",\["InstagramODS","PolarisAPIGetProfilePosts","PolarisAPIQuery","PolarisGenericStrings","PolarisLegacyGraphQLPaginationUtils","PolarisLogger","PolarisPaginationUtils","PolarisPostModel","PolarisProfileLogger","PolarisProfilePostsActionConstants","PolarisProfilePostsModel","PolarisProfilePostsSelectors.react","PolarisReelModel","PolarisUserModel","asyncToGeneratorRuntime","handlePolarisProfilePostsAPIResponse","justknobx","nullthrows","polarisGetUsersFromGraphMedia","polarisUnexpected"],\(function\(.*?\)\{"use strict";.*?=0;.*?="(.*?)";var', res)
                if len(DocID) > 0:
                    DocID = DocID[0]
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, DocID

    """
        辅助函数 获取WorkDocID
        获取DocID
        :param res_text: 主页html
        返回DocID
    """
    def get_WorkCommentDocID(self, url: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        CommentDocID = {
            "DocIDV1": None,
            "DocIDV2": None
        }
        try:
            headers = get_common_headers()
            cookies = trans_cookies_str_to_dict(cookies_str)
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
            res_text = response.text
            scripts_url = re.findall(r'<script src="(.*?)"', res_text)
            scripts_url = [url for url in scripts_url if url.startswith("http")]
            for url in scripts_url:
                response = requests.get(url, headers=headers, proxies=proxies)
                res = response.text
                DocIDV1 = re.findall(r'__d\("PolarisPostCommentsPaginationQuery_instagramRelayOperation",\[],\(function\(.*?\)\{e\.exports="(.*?)"}\),null\);', res)
                if len(DocIDV1) > 0:
                    CommentDocID["DocIDV1"] = DocIDV1[0]
                    continue
                DocIDV2 = re.findall(r'__d\("PolarisPostChildCommentsQuery_instagramRelayOperation",\[],\(function\(.*?\)\{e\.exports="(.*?)"}\),null\);', res)
                if len(DocIDV2) > 0:
                    CommentDocID["DocIDV2"] = DocIDV2[0]
                    continue
                if CommentDocID["DocIDV1"] is not None and CommentDocID["DocIDV2"] is not None:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, CommentDocID

    """
        每个用户的Xinfo是不一样的，所以每个用户查询前必须调用
        获取主要信息
        :param user_id: 你想要获取的用户的id
        返回主要信息
    """
    def get_info(self, username: str, proxies: dict = None):
        success = True
        msg = '成功'
        Xinfo_res = None
        try:
            headers = get_common_headers()
            response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, proxies=proxies)
            res_text = response.text
            user_id = re.findall(r'"user_id":"(.*?)"', res_text)[0]
            XIgAppId = re.findall(r'"app_id":"(.*?)"', res_text)[0]
            success, msg, HomeDocID = self.get_HomeProfileDocID(res_text)
            Xinfo_res = {
                "user_name": username,
                "user_id": user_id,
                "XIgAppId": XIgAppId,
                "HomeDocID": HomeDocID
            }
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, Xinfo_res

    """
        获取用户的信息
        :param Xinfo: 你想要获取的用户Info
        返回用户的信息
    """
    def get_user_info(self, user_name: str, XIgAppId: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        res_json = None
        try:
            url = "https://www.instagram.com/api/v1/users/web_profile_info/"
            params = {
                "username": user_name
            }
            cookies = trans_cookies_str_to_dict(cookies_str)
            headers = get_requests_userinfo_headers(XIgAppId)
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            res_json = response.json()
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取用户指定位置的视频
        :param Xinfo: 你想要获取的用户Info
        返回用户指定位置的视频
    """
    def get_user_videos(self, user_id: str, DocID: str, after: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        res = None
        try:
            url = "https://www.instagram.com/graphql/query/"
            variables = {
                "id": str(user_id),
                "first": 12,
                "after": after
            }
            variables_str = json.dumps(variables)
            params = {
                "doc_id": DocID,
                "variables": variables_str,
            }
            cookies = trans_cookies_str_to_dict(cookies_str)
            headers = get_common_headers()
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            res_json = response.json()
            data = res_json["data"]["user"]["edge_owner_to_timeline_media"]
            has_next_page = data["page_info"]["has_next_page"]
            end_cursor = data["page_info"]["end_cursor"]
            urls = [f'https://www.instagram.com/reel/{one["node"]["shortcode"]}/' for one in data["edges"]]
            res = {
                "has_next_page": has_next_page,
                "end_cursor": end_cursor,
                "urls": urls
            }
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

    """
        获取用户所有视频
        :param Xinfo: 你想要获取的用户Info
        返回用户所有视频
    """
    def get_user_all_videos(self, user_id: str, DocID: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        urls = []
        try:
            after = ""
            while True:
                success, msg, res = self.get_user_videos(user_id, DocID, after, cookies_str, proxies)
                if not success:
                    break
                urls.extend(res["urls"])
                if not res["has_next_page"]:
                    break
                after = res["end_cursor"]
        except Exception as e:
            success = False
        return success, urls

    """
        获取作品指定位置的一级评论
        :param Xinfo: 你想要获取的用户Info
        返回作品指定位置的一级评论
    """
    def get_work_outer_comments(self, DocID: str, mediaID: str, after: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        res = None
        try:
            url = "https://www.instagram.com/graphql/query/"
            variables = {
                "after": after,
                "before": None,
                "first": 10,
                "last": None,
                "media_id": mediaID,
                "sort_order": "popular"
            }
            variables_str = json.dumps(variables)
            data = {
                "variables": variables_str,
                "doc_id": DocID
            }
            cookies = trans_cookies_str_to_dict(cookies_str)
            headers = get_common_headers()
            response = requests.post(url, headers=headers, cookies=cookies, data=data, proxies=proxies)
            res_json = response.json()
            data = res_json["data"]["xdt_api__v1__media__media_id__comments__connection"]
            has_next_page = data["page_info"]["has_next_page"]
            end_cursor = data["page_info"]["end_cursor"]
            comments = [comment for comment in data["edges"]]
            res = {
                "has_next_page": has_next_page,
                "end_cursor": end_cursor,
                "comments": comments
            }
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

    """
        获取用户所有一级评论
        :param Xinfo: 你想要获取的用户Info
        返回用户所有一级评论
    """
    def get_work_all_outer_comments(self, DocID: str, mediaID: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        comments = []
        try:
            after = ""
            while True:
                success, msg, res = self.get_work_outer_comments(DocID, mediaID, after, cookies_str, proxies)
                if not success:
                    break
                comments.extend(res["comments"])
                if not res["has_next_page"]:
                    break
                after = res["end_cursor"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, comments

    """
        获取作品指定位置的二级评论
        :param Xinfo: 你想要获取的用户Info
        返回作品指定位置的二级评论
    """
    def get_work_inner_comments(self, DocID: str, mediaID: str, after: str, parent_comment_id: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        res = None
        try:
            url = "https://www.instagram.com/graphql/query/"
            variables = {
                "after": after,
                "before": None,
                "media_id": mediaID,
                "parent_comment_id": parent_comment_id,
                "is_chronological": None,
                "first": None,
                "last": None
            }
            variables_str = json.dumps(variables)
            data = {
                "variables": variables_str,
                "doc_id": DocID
            }
            cookies = trans_cookies_str_to_dict(cookies_str)
            headers = get_common_headers()
            response = requests.post(url, headers=headers, cookies=cookies, data=data, proxies=proxies)
            res_json = response.json()
            data = res_json["data"]["xdt_api__v1__media__media_id__comments__parent_comment_id__child_comments__connection"]
            has_next_page = data["page_info"]["has_next_page"]
            end_cursor = data["page_info"]["end_cursor"]
            comments = [comment for comment in data["edges"]]
            res = {
                "has_next_page": has_next_page,
                "end_cursor": end_cursor,
                "comments": comments
            }
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

    """
        获取用户所有二级评论
        :param Xinfo: 你想要获取的用户Info
        返回用户所有二级评论
    """
    def get_work_all_inner_comments(self, DocID: str, mediaID: str, parent_comment_id: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        comments = []
        try:
            after = ""
            while True:
                success, msg, res = self.get_work_inner_comments(DocID, mediaID, after, parent_comment_id, cookies_str, proxies)
                if not success:
                    break
                comments.extend(res["comments"])
                if not res["has_next_page"]:
                    break
                after = res["end_cursor"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, comments

    """
        获取用户所有评论
        :param Xinfo: 你想要获取的用户Info
        返回用户所有评论
    """
    def get_work_all_comments(self, CommentDocID: dict, mediaID: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        comments = None
        try:
            success, msg, comments = self.get_work_all_outer_comments(CommentDocID["DocIDV1"], mediaID, cookies_str, proxies)
            if not success:
                return success, comments
            for comment in comments:
                if comment["node"]["child_comment_count"] > 0:
                    success, msg, res = self.get_work_all_inner_comments(CommentDocID["DocIDV2"], mediaID, comment["node"]["pk"], cookies_str, proxies)
                    if not success:
                        print(2)
                        return success, res
                    comment["node"]["sub_comments"] = res
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, comments

    """
        获取一篇ins的详细信息
        :param Xinfo: 你想要获取的用户Info
        返回一篇ins的详细信息
    """
    def get_inswork_info(self, url: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = '成功'
        res = None
        try:
            headers = get_common_headers()
            cookies = trans_cookies_str_to_dict(cookies_str)
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
            res = response.text
            data = re.findall('"result":\{"data":\{"xdt_api__v1__media__shortcode__web_info":\{"items":\[(.*)]}},"extensions":\{"is_final":true}}', res)[0]
            res = json.loads(data)
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

if __name__ == '__main__':
    # =====================================================================
    # |                                          |
    # |                                                                    |
    # |      获取用户信息、 获取用户所有视频                                    |
    # |      需要首先调用get_info获取用户的一些必要信息！每个用户不同             |
    # |                                                                    |
    # |      获取作品的全部评论                                             |
    # |      需要首先调用get_WorkCommentDocID获取作品的一些必要信息！每个作品不同  |
    # |                                                                     |
    # ======================================================================
    ins_apis = INS_Apis()
    cookies_str = r''
    # 获取用户主要信息（每个用户查询前必须调用）
    # success, msg, Xinfo = ins_apis.get_info("daniel_xueyx")
    # print(success, msg, Xinfo)
    # # 获取用户信息
    # success, msg, res = ins_apis.get_user_info("daniel_xueyx", Xinfo["XIgAppId"], cookies_str)
    # print(success, msg, res)
    # 获取用户所有视频
    # success, msg, res = ins_apis.get_user_all_videos(Xinfo["user_id"], Xinfo["HomeDocID"], cookies_str)
    # print(success, msg, res)
    # print(len(res))

    ################################################################################################################################

    # 获取一篇ins的详细信息
    url = 'https://www.instagram.com/reel/C56MpyPrO_3/'
    success, msg, res = ins_apis.get_inswork_info(url, cookies_str)
    media_id = res["pk"]
    print(media_id)
    print(success, msg, str(res).replace('\'', '\"'))
    # # 获取一篇ins的DocID
    # success, msg, CommentDocID = ins_apis.get_WorkCommentDocID(url, cookies_str)
    # print(success, msg, CommentDocID)
    # # 获取作品的全部评论
    # success, msg, res = ins_apis.get_work_all_comments(CommentDocID, media_id, cookies_str)
    # print(success, msg, res)
