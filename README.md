# URL Cleaner

## Introduction

A package for removing tracing parameters from URLs. This package supports:
- Automatically updating filtering rules from Adguard.
- Custom filtering rules.
- Host pathname specific filtering.

## Examples

原始： https://baijiahao.baidu.com/s?id=1748839822649920321&wfr=spider&for=pc
清除后： https://baijiahao.baidu.com/s?id=1748839822649920321

原始： https://mp.weixin.qq.com/s?__biz=MjM5OTExMjYwMA==&mid=2670081058&idx=6&sn=1ad7112020c2a4104d67ca542ab14444&chksm=bc12eed58b6567c30c78123a9e8901241512642305dabae4fa1f52357f5ce0ac7a85554#rd
清除后： https://mp.weixin.qq.com/s?__biz=MjM5OTExMjYwMA%3D%3D&mid=2670081058&idx=6&sn=1ad7112020c2a4104d67ca542ab14444#rd

原始： https://www.bilibili.com/video/BV158411b7ki/?spm_id_from=333234107.tianma.1-2-2.click
清除后： https://www.bilibili.com/video/BV158411b7ki/

## Usage

### Clean URLs

```
from url_cleaner import UrlCleaner
c = UrlCleaner()
url = "https://baijiahao.baidu.com/s?id=1748839822649920321&wfr=spider&for=pc"
cleaned = c.clean(url)
print(cleaned)
```

> https://baijiahao.baidu.com/s?id=1748839822649920321

### Update rules

```
from url_cleaner import UrlCleaner
c = UrlCleaner()
c.ruler.update_rules()
```
