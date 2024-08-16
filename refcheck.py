import requests
import uuid
import argparse
from urllib.parse import urlparse, urlunparse
import time
import urllib3
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


print(r"""
                    ______           __                         __       
                   /      \         |  \                       |  \      
  ______   ______ |  ▓▓▓▓▓▓\ _______| ▓▓____   ______   _______| ▓▓   __ 
 /      \ /      \| ▓▓_  \▓▓/       \ ▓▓    \ /      \ /       \ ▓▓  /  \
|  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓ \   |  ▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓\  ▓▓▓▓▓▓\  ▓▓▓▓▓▓▓ ▓▓_/  ▓▓
| ▓▓   \▓▓ ▓▓    ▓▓ ▓▓▓▓   | ▓▓     | ▓▓  | ▓▓ ▓▓    ▓▓ ▓▓     | ▓▓   ▓▓ 
| ▓▓     | ▓▓▓▓▓▓▓▓ ▓▓     | ▓▓_____| ▓▓  | ▓▓ ▓▓▓▓▓▓▓▓ ▓▓_____| ▓▓▓▓▓▓\ 
| ▓▓      \▓▓     \ ▓▓      \▓▓     \ ▓▓  | ▓▓\▓▓     \\▓▓     \ ▓▓  \▓▓\
 \▓▓       \▓▓▓▓▓▓▓\▓▓       \▓▓▓▓▓▓▓\▓▓   \▓▓ \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓   \▓▓
                                                       By @NEXIZ0    V2.1


""")



# Initialize global variables
found_any = False
post_plotion = False
get_plotion = False
boundary = f'----WebKitFormBoundary{uuid.uuid4().hex}'
found_urls = []
count = 0

c1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    'Content-Type': 'application/x-www-form-urlencoded'
}

c2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    'Content-Type': 'text/plain'
}

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

def get_base_url(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, None, None, None))

def p1(url, base_url, params, cookies):
    #double_quote
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%22a"
    sen1  = 'nexiz"a"'
    res1 = ['nexiz"a"', 'nexiz\\"a"', 'nexiz\"a"']

    progress_bar = tqdm(params, desc=f"Checking %22", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[\"]_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)

        url_get_plo_t = f"{url}&{param}=test&{param}=nexiz"
        responset = requests.get(url_get_plo_t, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        if "nexiz" in responset.text:
            get_plotion = True
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={sen1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: sen1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart => {par1}\033[0m")
        time.sleep(1.5)

        datas = {param: ['test', 'nexiz']}
        response = requests.post(base_url, headers=c1, data=datas, cookies=cookies, allow_redirects=True, verify=False)
        if "nexiz" in response.text:
            post_plotion = True
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={sen1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', sen1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: polotion multypart => {par1}")
                print(f"\033[91mPOST: polotion multypart => {par1}\033[0m")
            time.sleep(1.5)
    

def p2(url, base_url, params, cookies):
    #single_quote
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%27a"
    sen1 = "nexiz'a'"
    res1 = ["nexiz'a'", "nexiz\\'a'", "nexiz\'a'"]

    progress_bar = tqdm(params, desc=f"Checking %27", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[\']_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: sen1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={sen1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: sen1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={sen1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', sen1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p3(url, base_url, params, cookies):
    #Less-Than_Sign"<"
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%3Cx"
    res1 = "nexiz<x"

    progress_bar = tqdm(params, desc=f"Checking <", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[<]_on_({param})", refresh=True)
        if res1 in response.text:
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={res1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: res1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={res1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', res1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p4(url, base_url, params, cookies):
    #double_quote_html_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%26%2334%3Ba"
    tes1  = "nexiz&#34;a"
    res1 = ['nexiz"a"', 'nexiz\\"a"', 'nexiz\"a"']

    progress_bar = tqdm(params, desc=f"Checking Htmlencode %22", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[H-\"]_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: tes1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', tes1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p5(url, base_url, params, cookies):
    #single_quote_html_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%26%2339%3Ba"
    tes1  = "nexiz&#39;a"
    res1 = ["nexiz'a'", "nexiz\\'a'", "nexiz\'a'"]

    progress_bar = tqdm(params, desc=f"Checking Htmlencod %27", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[H-\']_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: tes1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', tes1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p6(url, base_url, params, cookies):
    #"<"_html_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%26%2360%3Bx"
    tes1  = "nexiz&#60;x"
    res1 = "nexiz<x"

    progress_bar = tqdm(params, desc=f"Checking Htmlencode <", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[H - <]_on_({param})", refresh=True)
        if res1 in response.text:
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: tes1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', tes1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p7(url, base_url, params, cookies):
    #double_quote_double_url_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%2522a"
    res1 = ['nexiz"a"', 'nexiz\\"a"', 'nexiz\"a"']

    progress_bar = tqdm(params, desc=f"Checking Double %22", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[D-\"]_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: par1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', par1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p8(url, base_url, params, cookies):
    #single_quote_double_url_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%2527a"
    res1 = ["nexiz'a'", "nexiz\\'a'", "nexiz\'a'"]

    progress_bar = tqdm(params, desc=f"Checking Double %27", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[D-\']_on_({param})", refresh=True)
        if any(r in response.text for r in res1):
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: par1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if any(r in response.text for r in res1):
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', par1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if any(r in response.text for r in res1):
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p9(url, base_url, params, cookies):
    #"<"_double_url_encode
    global found_any, get_plotion, post_plotion, boundary, count

    par1 = "nexiz%253Cx"
    res1 = "nexiz<x"

    progress_bar = tqdm(params, desc=f"Checking double-encode <", unit="request", colour='green')

    for param in progress_bar:
        url_g = f"{url}&{param}={par1}"
        response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
        progress_bar.set_description(f"Checking_[D - <]_on_({param})", refresh=True)
        if res1 in response.text:
            count += 1
            found_any = True
            found_urls.append(url_g)
            print(f"\033[91m{url_g}\033[0m")
        time.sleep(1.5)


        if (get_plotion == True):
            url_get_plo = f"{url}&{param}=test&{param}={par1}"
            response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(url_get_plo)
                print(f"\033[91m{url_get_plo}\033[0m")
        time.sleep(1.5)

        data_url_encoded = {param: par1}
        response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: url_encoded => {data_url_encoded}")
            print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
        time.sleep(1.5)

        data_text_plain = f"{param}={par1}"
        response = requests.post(base_url, data=data_text_plain, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: text_plain => {data_text_plain}")
            print(f"\033[91mPOST: text_plain => {data_text_plain}\033[0m")
        time.sleep(1.5)

        form_data = {param: par1}
        lines = []
        for name, value in form_data.items():
            lines.extend([
                f"--{boundary}",
                f"Content-Disposition: form-data; name=\"{name}\"",
                "",
                value
            ])
        lines.append(f"--{boundary}--")
        ppayload = "\r\n".join(lines)
        headpos = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(ppayload))
        }
        response = requests.post(base_url, data=ppayload, headers=headpos, cookies=cookies, allow_redirects=True, verify=False)
        if res1 in response.text:
            found_any = True
            count += 1
            found_urls.append(f"POST: multypart_simple => {par1}")
            print(f"\033[91mPOST: multypart_simple => {par1}\033[0m")
        time.sleep(1.5)

        if (post_plotion == True):
            dataz = {param: ['test', par1]}
            response = requests.post(base_url, headers=c1, data=dataz, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST plotion url_encoded: {dataz}")
                print(f"\033[91mPOST plotion url_encoded: {dataz}\033[0m")
            time.sleep(1.5)

            data_text_plain_p = f"{param}=test&{param}={par1}"
            response = requests.post(base_url, data=data_text_plain_p, headers=c2, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion text_plain => {data_text_plain_p}")
                print(f"\033[91mPOST: plosion text_plain => {data_text_plain_p}\033[0m")
            time.sleep(1.5)

            form_data_p = {param: ['test', par1]}
            lines_p = []
            for name, values in form_data_p.items():
                for value in values:
                    lines_p.extend([
                        f"--{boundary}",
                        f"Content-Disposition: form-data; name=\"{name}\"",
                        "",
                        value
                    ])
            lines_p.append(f"--{boundary}--")
            payload = "\r\n".join(lines_p)
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(payload))
            }
            response = requests.post(base_url, data=payload, headers=headers, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: plosion multypart => {par1}")
                print(f"\033[91mPOST : polotion multypart=> {par1}\033[0m")
            time.sleep(1.5)

def p10(url, base_url, params, cookies):
    global found_any, get_plotion, post_plotion, boundary, count, found_urls, head, c1

    par = ["%3C%25=901%2A1100%25%3E", "%7B%7B901%2A1100%7D%7D", "%24%7B901%2A1100%7D",
           "%40%28901%2A1100%29", "%24%7B%7B901%2A1100%7D%7D", "%23%7B901%2A1100%7D"]

    res1 = "991100"

    progress_bar = tqdm(params, desc=f"Checking SSTI", unit="request", colour='green')

    for param in progress_bar:
        for par1 in par:
            url_g = f"{url}&{param}={par1}"
            response = requests.get(url_g, headers=head, cookies=cookies, allow_redirects=True, verify=False)
            progress_bar.set_description(f"Checking SSTI on ({param})", refresh=True)
            if res1 in response.text:
                count += 1
                found_any = True
                found_urls.append(url_g)
                print(f"\033[91m{url_g}\033[0m")
            time.sleep(1.5)

            if get_plotion:
                url_get_plo = f"{url}&{param}=test&{param}={par1}"
                response = requests.get(url_get_plo, headers=head, cookies=cookies, allow_redirects=True, verify=False)
                if res1 in response.text:
                    found_any = True
                    count += 1
                    found_urls.append(url_get_plo)
                    print(f"\033[91m{url_get_plo}\033[0m")
            time.sleep(1.5)

            data_url_encoded = {param: par1}
            response = requests.post(base_url, data=data_url_encoded, headers=c1, cookies=cookies, allow_redirects=True, verify=False)
            if res1 in response.text:
                found_any = True
                count += 1
                found_urls.append(f"POST: url_encoded => {data_url_encoded}")
                print(f"\033[91mPOST: url_encoded => {data_url_encoded}\033[0m")
            time.sleep(1.5)


def main():
    parser = argparse.ArgumentParser(description="Process URL and parameters.")
    parser.add_argument('-u', '--url', type=str, required=True, help='URL')
    parser.add_argument('-p', '--params', type=str, help='Comma-separated parameters')
    parser.add_argument('-r', '--readfile', type=str, help='File containing parameters, one per line')
    parser.add_argument('--http2', action='store_true', help='Use HTTP/2 prefix')

    args = parser.parse_args()
    url = args.url

    params = []
    base_url = get_base_url(url)

    global count, found_urls

    if args.params:
        params = args.params.split(',')
    elif args.readfile:
        try:
            with open(args.readfile, 'r') as file:
                params = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: The file {args.readfile} was not found.")
            return
    else:
        print("Error: No parameters provided. Use -p or -r option.")
        return

    # Send initial GET request to base URL to capture cookies
    initial_response = requests.get(base_url, headers=head, allow_redirects=False, verify=False)
    cookies = initial_response.cookies
    second_response = requests.get(base_url, headers=head, cookies=cookies, allow_redirects=True, verify=False)
    cookies.update(second_response.cookies)

    if args.http2:
        print("Comming Soon!!!")
    else:
        p1(url, base_url, params, cookies)
        p2(url, base_url, params, cookies)
        p3(url, base_url, params, cookies)
        p4(url, base_url, params, cookies)
        p5(url, base_url, params, cookies)
        p6(url, base_url, params, cookies)
        p7(url, base_url, params, cookies)
        p8(url, base_url, params, cookies)
        p9(url, base_url, params, cookies)
        p10(url, base_url, params, cookies)
        print(f"\033[91mpossible {count} injection\033[0m")

if __name__ == "__main__":
    main()
