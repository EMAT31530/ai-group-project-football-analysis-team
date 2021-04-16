import requests
from requests.exceptions import RequestException
import json
import csv
import time
import random

# 获取页面内容
def get_page(match_url, headers):
    try:
        response = requests.get(match_url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException as err:
        print('获取页面错误')
        print(err)

# 解析页面数据
def parse_page(html):
    # 解析返回的Json数据
    html = json.loads(html)

    # 比赛双方存储数据的list
    team_1_list = ['name', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    team_2_list = ['name', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 比赛双方球队名字
    team_1_list[0] = html['entity']['teams'][0]['team']['name']
    team_2_list[0] = html['entity']['teams'][1]['team']['name']

    # 比赛双方球队id
    id_1 = str(html['entity']['teams'][0]['team']['club']['id'])
    id_2 = str(html['entity']['teams'][1]['team']['club']['id'])

    # 比赛双方球队的进球数
    score_1 = html['entity']['teams'][0]['score']
    score_2 = html['entity']['teams'][1]['score']

    # list中存储比赛结果：1为赢球，-1为输球，0为平
    if score_1 > score_2:
        team_1_list[15] = 1
        team_2_list[15] = -1
    elif score_1 < score_2:
        team_1_list[15] = -1
        team_2_list[15] = 1
    elif score_1 == score_2:
        team_1_list[15] = 0
        team_2_list[15] = 0

    # 从网页中解析比赛数据
    for item in html['data'][id_1]['M']:
        if item['name'] == 'accurate_pass':
            # 比赛数据:accurate pass
            team_1_list[1] = item['value']
        elif item['name'] == 'possession_percentage':
            # 比赛数据:possession percentage
            team_1_list[2] = item['value']
        elif item['name'] == 'touches':
            # 比赛数据:touches
            team_1_list[3] = item['value']
        elif item['name'] == 'total_pass':
            # 比赛数据:total pass
            team_1_list[4] = item['value']
        elif item['name'] == 'fk_foul_lost':
            # 比赛数据:Fouls conceded
            team_1_list[5] = item['value']
        elif item['name'] == 'shot_off_target':
            # 比赛数据:shot off target
            team_1_list[6] = item['value']
        elif item['name'] == 'offtarget_att_assist':
            # 比赛数据:off target assist
            team_1_list[7] = item['value']
        elif item['name'] == 'ontarget_scoring_att':
            # 比赛数据:score on target
            team_1_list[8] = item['value']
        elif item['name'] == 'won_corners':
            # 比赛数据:won corners
            team_1_list[9] = item['value']
        elif item['name'] == 'total_tackle':
            # 比赛数据:total tackle
            team_1_list[10] = item['value']
        elif item['name'] == 'total_clearance':
            # 比赛数据:total clearance
            team_1_list[11] = item['value']
        elif item['name'] == 'total_yel_card':
            # 比赛数据:total yellow cards
            team_1_list[12] = item['value']
        elif item['name'] == 'total_offside':
            # 比赛数据:total offside
            team_1_list[13] = item['value']
        elif item['name'] == 'ontarget_att_assist':
            # 比赛数据:on target assist
            team_1_list[14] = item['value']
    
    # 重复上述过程
    for item in html['data'][id_2]['M']:
        if item['name'] == 'accurate_pass':
            team_2_list[1] = item['value']
        elif item['name'] == 'possession_percentage':
            team_2_list[2] = item['value']
        elif item['name'] == 'touches':
            team_2_list[3] = item['value']
        elif item['name'] == 'total_pass':
            team_2_list[4] = item['value']
        elif item['name'] == 'fk_foul_lost':
            team_2_list[5] = item['value']
        elif item['name'] == 'shot_off_target':
            team_2_list[6] = item['value']
        elif item['name'] == 'offtarget_att_assist':
            team_2_list[7] = item['value']
        elif item['name'] == 'ontarget_scoring_att':
            team_2_list[8] = item['value']
        elif item['name'] == 'won_corners':
            team_2_list[9] = item['value']
        elif item['name'] == 'total_tackle':
            team_2_list[10] = item['value']
        elif item['name'] == 'total_clearance':
            team_2_list[11] = item['value']
        elif item['name'] == 'total_yel_card':
            team_2_list[12] = item['value']
        elif item['name'] == 'total_offside':
            team_2_list[13] = item['value']
        elif item['name'] == 'ontarget_att_assist':
            team_2_list[14] = item['value']
    
    # 返回比赛双方数据列表
    return team_1_list, team_2_list

# 将数据存入文件
def write2csv(data):
    with open('all_data.csv','a',newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == "__main__":
    # 模拟浏览器表头  
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.premierleague.com',
        'Referer': 'https://www.premierleague.com/',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }

    user_agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ]
    
    # 构造英超比赛网页url
    team_1, team_2 = [], []
    for index in range(46605, 46985):
        match_url = "https://footballapi.pulselive.com/football/stats/match/" + str(index)
        # 获取比赛网页
        user_agent = random.choice(user_agent_list)
        headers['User-Agent'] = user_agent
        html = get_page(match_url, headers)
        # 解析比赛网页数据
        team_1_list, team_2_list = parse_page(html)
        team_1.append(team_1_list)
        team_2.append(team_2_list)
        write2csv(team_1_list)
        write2csv(team_2_list)
        print(index)
        time.sleep(random.randint(10, 20))


