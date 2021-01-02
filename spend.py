import requests,time,sys,os,re
import xml.etree.ElementTree as ET
from jinja2 import FileSystemLoader, Environment
from pprint import pprint

pattern = re.compile('//(.+:\d+)/job/(.+)?/(\d+)?/')
m = re.search(pattern,sys.argv[1])
remote_ip = m.group(1)
project_name = m.group(2)
build_no = m.group(3)
password = '123456'
username = 'xpc'
# remote_ip = 'localhost:8080'
# project_name = 'yj'
crumb_url = f'http://{username}:{password}@{remote_ip}/crumbIssuer/api/json'
# query_build_no_url = f'http://{username}:{password}@{remote_ip}/job/{project_name}/lastBuild/buildNumber'
fa = pa = tot = rate = 0
result = '--'

# 测试结束后报告不是立马生成的，此时需要检查是否有报告生成，并获取用例的关键信息
wait_time = 60
while wait_time > 0:
    if os.path.isfile('./report.html') and os.path.isfile('./output.xml'):
        print('report.html created')
        tree = ET.parse('./output.xml')
        statistics = tree.find('statistics')
        total = statistics.find('total')
        for item in total:
            if 'All Tests' == item.text:
                fa = int(item.attrib['fail'])
                pa = int(item.attrib['pass'])
                tot = fa + pa
                rate = '%.2f' % (pa * 100 / tot)
                if fa != 0:
                    result = 'Fail'
                else:
                    result = 'Pass'
        break
    time.sleep(1)
    wait_time -= 1
# 渲染模板
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('template.html')
html = template.render(
    project_name='yj',
    fa=fa,
    pa=pa,
    tot=tot,
    rate=rate,
    result=result,
    build_no=build_no,
    build_url=sys.argv[1],
    log_url=os.path.join(os.getcwd(),'log.html')
)
with open('daily_report.html','w',encoding='utf8') as f:
    f.write(html)

# 对测试的时间进行检查，过短则发送构建失败的邮件
ret1 = requests.get(crumb_url)
headers ={'Jenkins-Crumb':ret1.json()['crumb']}
# last_build = requests.get(query_build_no_url,headers=headers)
# 十三位时间戳
time_now = round(time.time()*1000)
url = f'http://{username}:{password}@{remote_ip}/job/{project_name}/wfapi/runs?since=%23{build_no}&fullStages=true'
ret2 = requests.get(url,headers=headers)
last_build_stages = ret2.json()[0]['stages']
spend = int(last_build_stages[-1]['durationMillis'])/1000

if spend < 60000:
    raise Exception('本次构建时间过短')