
def get_common_headers():
    return {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "dpr": "0.9",
        "sec-ch-prefers-color-scheme": "light",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"123.0.2420.81\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.106\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"15.0.0\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        "viewport-width": "351"
    }

def get_requests_userinfo_headers(XIgAppId):
    return {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "dpr": "0.9",
        "referer": f"https://www.instagram.com/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"123.0.2420.81\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.106\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"15.0.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        "viewport-width": "225",
        "x-ig-app-id": XIgAppId,
        "x-requested-with": "XMLHttpRequest"
    }

def get_requests_userwork_headers(info):
    username = info["user_name"]
    Xsrftoken = info["Xsrftoken"]
    XIgAppId = info["XIgAppId"]
    XIgWwwClaim = info["XIgWwwClaim"]
    return {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "dpr": "1",
        "pragma": "no-cache",
        "referer": f"https://www.instagram.com/{username}/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"123.0.6312.106\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.106\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"15.0.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "viewport-width": "723",
        "x-asbd-id": "129477",
        "x-csrftoken": Xsrftoken,
        "x-ig-app-id": XIgAppId,
        "x-ig-www-claim": XIgWwwClaim,
        "x-fb-friendly-name": "PolarisProfilePostsTabContentQuery_connection",
        "x-requested-with": "XMLHttpRequest",
    }

def get_requests_comment_headers(info):
    username = info["user_name"]
    Xsrftoken = info["Xsrftoken"]
    XIgAppId = info["XIgAppId"]
    XIgWwwClaim = info["XIgWwwClaim"]
    return {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "dpr": "0.9",
        "origin": "https://www.instagram.com",
        "referer": f"https://www.instagram.com/p/{username}/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"123.0.2420.81\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.106\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"15.0.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        "viewport-width": "832",
        "x-asbd-id": "129477",
        "x-ig-www-claim": XIgWwwClaim,
        "x-csrftoken": Xsrftoken,
        "x-fb-friendly-name": "PolarisPostCommentsPaginationQuery",
        "x-ig-app-id": XIgAppId,
    }
def trans_cookies_str_to_dict(cookies_str: str):
    return {item.split("=")[0]: item.split("=")[1] for item in cookies_str.split("; ")}