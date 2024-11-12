# Data Folder Overview

This folder contains several JSON files, primarily including `regulations.json`, `results.json`, and `policy.json`. These files contain information crawled from the customs website, specifically:

- **regulations.json**: Contains regulatory data, detailing the type, category, announcement number, issuing authority, issue date, effective date, status, remarks, title, and content of the regulations.
- **results.json**: Contains data on collection results, recording the title and specific content of the interpretations.
- **policy.json**: Contains policy interpretation data, recording the title and specific content of the interpretations.

These data can be used for analysis and research on customs-related regulations and policies.


## regulations.json
The file `regulations.json` contains regulatory data crawled from the customs website. The data structure is as follows:
- **document_type**: A string, the type of the regulation.
- **category**: A string, the type of the regulation.
- **announcement_number**: A string, the announcement_number of the regulation.
- **issuing_authority**: A string, the authority that issues the regulation.
- **issue_date**: A string, the date the regulation was published, in the format of `YYYY-MM-DD`.
- **effective_date**: A string, the date the regulation was effected, in the format of `YYYY-MM-DD`.
- **status**: A string, the effective status of regulation.
- **remark**: A string, the supplementary information on the effective status of the regulation.
- **title**: A string, the title of the regulation.
- **content**: A string, the specific content of the regulation.

## Example
```json
[
    {
        "document_type": "海关规范性文件",
        "category": "其他",
        "announcement_number": "公告〔2023〕199号",
        "issuing_authority": "海关总署",
        "issue_date": "2023-12-29",
        "effective_date": "2024-02-01",
        "status": "有效",
        "remarks": "",
        "title": "海关总署公告2023年第199号（关于推进《内地海关及香港海关陆路进/出境载货清单》无纸化工作的公告）",
        "content": "为促进内港两地经济发展，方便两地经贸往来，进一步简化海关监管手续，海关总署决定进一步推进《内地海关及香港海关陆路进/出境载货清单》（以下简称《载货清单》）无纸化工作。现就有关事项公告如下：企业在向内地海关办理内地、香港陆路货运车辆（含货运空车）和所载货物各项通关监管手续时，无需提交纸质《载货清单》。《载货清单》的其他相关事项仍按照海关总署公告2004年第42号执行。本公告自2024年2月1日起施行。特此公告。海关总署2023年12月29日"
    }
]
```

## result.json
The file `result.json` contains the interpretation result data. The data structure is as follows:
- **title**: string, title of the solicitation result.
- **content**: string, content of the solicitation result.

## Example
```json
[
    {
        "title": "关于《中华人民共和国海关行政处罚裁量基准（三）（征求意见稿）》公开征求社会意见情况的反馈",
        "content": "2023年8月30日到9月30日，我署通过门户网站，就《中华人民共和国海关行政处罚裁量基准（三）（征求意见稿）》向社会公开征求意见。征求意见结束后，共收到有效反馈意见3条，主要涉及调整适用范围、修改相关定义等方面。经研究，部分采纳意见1条，不予采纳意见2条。部分采纳的意见主要为：对“轻微违法不予处罚”规定的进出口侵权货物的数量和价值进行了限定，并对多次实施违法行为的情形进行了规定。不予采纳的意见及理由主要为：一是部分意见内容涉及“从重处罚”中再犯情节的相关规定。不予采纳的原因已告知提议人，提议人表示理解和认可，已达成一致意见。二是部分意见内容涉及“初次违法”的定义范围。《民法典》规定的诉讼时效适用于民事案件，本裁量基准的适用范围为海关行政处罚案件，因此依据《行政处罚法》规定的行政违法追诉时效确定“初次违法”的时间认定标准。感谢社会各界对海关工作的关心支持！"
    }
]
```
## policys.json
The file `policys.json` contains the interpretation result data. The data structure is as follows:
- **title**: string, the title of the policy interpretation.
- **content**: string, the content of the policy interpretation.

## Example
```json
[
    {
        "title": "关于《海关总署 财政部 商务部 文化和旅游部 税务总局关于明确市内免税店经营品种的公告》的政策解读",
        "content": "一、背景依据《市内免税店管理暂行办法》第九条明确“市内免税店主要销售食品、服装服饰、箱包、鞋帽、母婴用品、首饰和工艺品、电子产品、香化产品、酒等便于携带的消费品。免税商品的经营范围，严格限于海关核定的种类和品种，核定工作由海关总署会同财政部、商务部、文化和旅游部、税务总局实施。鼓励市内免税店销售国货‘潮品’，将具有自主品牌、有助于传播中华优秀传统文化的特色产品纳入经营范围。”二、目标任务明确市内免税店经营品类范围，进一步规范市内免税店管理工作。三、主要内容市内免税店经营品种如下：1.食品、饮料；2.酒；3.纺织品及其制成品；4.皮革服装及配饰；5.箱包及鞋靴；6.表、钟及其配件、附件；7.眼镜（含太阳镜）；8.首饰及珠宝玉石；9.化妆品、洗护用品；10.母婴用品；11.厨卫用具及小家电（不含手机）；12.家用医疗、保健及美容美发器材；13.摄影（像）设备及其配件、附件；14.计算机及其外围设备；15.可穿戴设备等电子消费产品（无线耳机；其他接收、转换并发送或再生音像或其他数据用的设备；视频游戏控制器及设备的零件及附件）；16.文具用品、玩具、游戏品、节日或其他娱乐用品；17.工艺品；18.乐器；19.运动用品。制作单位：海关总署口岸监管司"
    }
]
```
