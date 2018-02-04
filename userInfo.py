"""
*******************
CopyRight: Yi Zhang
All Rights Reserved
*******************
"""


def getUserInfo():
    userInfoList=[]
    for i in range(30):
        userInfo={
            'username': 201414600101+i,
            'password': '123456'
        }
        userInfoList.append(userInfo)
    for i in range(30):
        userInfo={
            'username': 201414600201+i,
            'password': '123456'
        }
        userInfoList.append(userInfo)

    return userInfoList

if __name__=="__main__":
    getUserInfo()
