"""
*******************
CopyRight: Yi Zhang
All Rights Reserved
*******************
"""
import userInfo
import crawler


def run():
    userInfoList = userInfo.getUserInfo()
    crawler.batch(userInfoList)

if __name__ == "__main__":
    run()
