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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }

    # 构造英超比赛网页url
    team_1, team_2 = [], []
    for index in range(46605, 46985):
    #for index in range(46605, 46607):
        print(index)
        match_url = "https://footballapi.pulselive.com/football/stats/match/" + str(index)
        # 获取比赛网页
        html = get_page(match_url, headers)
        # 解析比赛网页数据
        team_1_list, team_2_list = parse_page(html)
        team_1.append(team_1_list)
        team_2.append(team_2_list)
        write2csv(team_1_list)
        write2csv(team_2_list)
        time.sleep(random.randint(15, 30))


