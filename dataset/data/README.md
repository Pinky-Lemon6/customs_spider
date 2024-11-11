# Regulations Data Structure
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
    },
    {
        "document_type": "海关规范性文件",
        "category": "其他",
        "announcement_number": "公告〔2023〕202号",
        "issuing_authority": "海关总署",
        "issue_date": "2023-12-28",
        "effective_date": "2023-12-28",
        "status": "有效",
        "remarks": "",
        "title": "海关总署公告2023年第202号（关于发布《中华人民共和国海关对横琴粤澳深度合作区监管办法》的公告）",
        "content": "为贯彻落实《横琴粤澳深度合作区建设总体方案》要求，支持横琴粤澳深度合作区高质量发展，特制定《中华人民共和国海关对横琴粤澳深度合作区监管办法》，现予发布。特此公告。附件：中华人民共和国海关对横琴粤澳深度合作区监管办法.doc海关总署2023年12月28日"
    }
]
