"""
*******************
CopyRight: Yi Zhang
All Rights Reserved
*******************
"""
import requests
from bs4 import BeautifulSoup


def batch(userInfoList):
    for i in range(len(userInfoList)):
        try:
            crawl(userInfoList[i])
        except:
            print("*** network exception ***")


def crawl(userInfo):
    if login(userInfo):
        condition = crawlAnswer()
        show(userInfo,condition)
    else:
        print('studentID:'+str(userInfo.get('username'))+' login error')


def show(userInfo,condition):
    print('studentID:'+str(userInfo.get('username'))+" is "+condition)


def crawlAnswer():
    #爬取前先检测是否存在该课程，如不存在就不用爬取答案页面，以免引起异常
    check = sessions.post('http://elearning.ncst.edu.cn/meol/welcomepage/student/course_list_v8.jsp',headers = header)
    check_soup = BeautifulSoup(check.text,'html.parser')
    #print(check.content.decode("GBK"))
    if len(check_soup.find_all('a',attrs = {'href' : './homepage/course/course_index.jsp?courseId=18879'}))<1:
        return "no the course"

    answerPage = sessions.post('http://elearning.ncst.edu.cn/meol/common/hw/student/taskanswer.jsp?hwtid=5895',
                               headers=header)
    answer_soup = BeautifulSoup(answerPage.text, 'html.parser')
    '''
    <table cellpadding="0" cellspacing="0" class="infotable">
        <tr>
            <th>回答的内容</th>
        </tr>
        <tr>
            <td class="text">
                &nbsp;
                此处若出现hidden，即若整个页面出现两次hidden，则说明已提交作业
            </td>
        </tr>
    </table>
    此table为显示作业结果的控件
    '''
    answerPageSoup = answer_soup.find_all('input', attrs={'type': 'hidden'})
    if len(answerPageSoup) >= 2:
        return "Submitted answer： " + answerPageSoup[1]['value']
    else:
        return "Unsubmitted"

header= {
    'Host':'elearning.ncst.edu.cn',
    'Upgrade-Insecure-Requests':'1',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2700.0 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8'
    }

def login(userInfo):
    '''
    实现建立session，保存cookie
    '''
    global sessions
    sessions = requests.session()
    #从登陆页面采集logintoken
    login_page = sessions.get('http://elearning.ncst.edu.cn/meol/loginCheck.do' , headers = header)
    login_soup = BeautifulSoup(login_page.text,'html.parser')
    #登陆数据准备
    logintoken = login_soup.find_all('input',attrs = {'name' : 'logintoken'})[0]['value']
    post_info = {
    'logintoken':logintoken,
    'IPT_LOGINUSERNAME':str(userInfo.get('username')),
    'IPT_LOGINPASSWORD':userInfo.get('password')
    }
    #执行登陆操作
    login_re = sessions.post('http://elearning.ncst.edu.cn/meol/loginCheck.do',data=post_info,headers = header)
    login_re_soup = BeautifulSoup(login_re.text,'html.parser')
    #检查是否登陆成功，能找到logintoken说明登陆失败
    if len(login_re_soup.find_all('input',attrs = {'name' : 'logintoken'}))>0:
        return False
    else:
        return True