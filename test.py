from url_cleaner import UrlCleaner

if __name__ == '__main__':
    c = UrlCleaner()
    
    urls = [
        'https://baijiahao.baidu.com/s?id=1748839822649920321&wfr=spider&for=pc',
        'https://mp.weixin.qq.com/s?__biz=MjM5OTExMjYwMA==&mid=2670081058&idx=6&sn=1ad7112020c2a4104d67ca542ab14444&chksm=bc12eed58b6567c30c78123a9e890ed79b448f82642305dabae4fa1f507a57f5ce0ac7a85554#rd',
        'https://www.bilibili.com/video/BV158411b7ki/?spm_id_from=333.1007.tianma.1-2-2.click',
    ]

    for url in urls:
        print("原始：",url)
        cleaned = c.clean(url)
        print("清除后：",cleaned)
        print('================================')

    # Update rules
    c.ruler.update_rules(mode="specific")
    c.ruler.update_rules(mode="general")