# -*- coding: utf-8 -*-
"""
@author: ZZK
"""
import requests
import time
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import url as _url

subscriber = 'bcai'


def get_one_page(url):
    response = requests.get(url)
    print(response.status_code)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        print(response.status_code)
    print(response.status_code)
    if response.status_code == 200:
        return response.text

    return None


def send_email(title, content):
    # 发送者邮箱
    sender = '1310248516@qq.com'
    # 发送者的登陆用户名和密码
    user = '1310248516@qq.com'
    password = 'zpbqpzkrsgwigbah'  # dailyarxiv123
    # 发送者邮箱的SMTP服务器地址
    smtpserver = 'smtp.qq.com'
    # 接收者的邮箱地址
    receiver = _url.get_email(subscriber)  # receiver 可以是一个list

    msg = MIMEMultipart('alternative')

    part1 = MIMEText(content, 'plain', 'utf-8')
    # html = open('subject_file.html','r')
    # part2 = MIMEText(html.read(), 'html')

    msg.attach(part1)
    # msg.attach(part2)

    # 发送邮箱地址
    msg['From'] = sender
    # 收件箱地址
    msg['To'] = receiver
    # 主题
    msg['Subject'] = title

    smtp = smtplib.SMTP()  # 实例化SMTP对象
    smtp.connect(smtpserver, 25)  # （缺省）默认端口是25 也可以根据服务器进行设定
    smtp.login(user, password)  # 登陆smtp服务器
    smtp.sendmail(sender, receiver, msg.as_string())  # 发送邮件 ，这里有三个参数
    '''
    login()方法用来登录SMTP服务器，sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文
    是一个str，as_string()把MIMEText对象变成str。
    '''
    smtp.quit()


def main():
    """
    https://arxiv.org/search/advanced?advanced=
    &terms-0-operator=AND
    &terms-0-term=LSTM
    &terms-0-field=title
    &terms-1-operator=AND
    &terms-1-term=networks
    &terms-1-field=abstract
    &classification-computer_science=y
    &classification-physics_archives=all
    &classification-include_cross_list=include
    &date-year=
    &date-filter_by=date_range
    &date-from_date=2022-04
    &date-to_date=2022-08
    &date-date_type=submitted_date
    &abstracts=show&size=50
    &order=-announced_date_first


https://arxiv.org/search/advanced?advanced=
&terms-0-operator=AND
&terms-0-term=LSTM
&terms-0-field=abstract
&terms-1-operator=AND
&terms-1-term=lstm
&terms-1-field=title
&classification-computer_science=y
&classification-physics_archives=all
&classification-include_cross_list=include
&date-year=&date-filter_by=date_range
&date-from_date=2021-07
&date-to_date=2022-08
&date-date_type=submitted_date
&abstracts=show
&size=50
&order=-announced_date_first


https://arxiv.org/search/advanced?advanced=
&date-from_date=2021-07
&date-to_date=2022-07
&terms-0-operator=AND
&terms-0-term=lstm
&terms-0-field=title
&terms-1-operator=AND
&terms-1-term=lstm
&terms-1-field=abstract
&classification-mathematics=y


    """
    # 基础url
    # url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=LSTM&terms-0-field=title" \
    #       "&terms-1-operator=AND&terms-1-term=networks&terms-1-field=abstract&classification-computer_science=y" \
    #       "&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by" \
    #       "=date_range&date-from_date=2022-04&date-to_date=2022-08&date-date_type=submitted_date&abstracts=show&size" \
    #       "=50&order=-announced_date_first"

    url = _url.get_url(subscriber)
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.ol

    list_ids = content.find_all('p', class_='list-title is-inline-block')
    ids = [p.find("a").get_text() for p in list_ids]

    list_title = content.find_all('p', class_='title is-5 mathjax')
    titles = [t.get_text().strip() for t in list_title]

    list_authors = content.find_all('p', class_='authors')
    authors = [t.get_text().replace("\n", "") for t in list_authors]
    authors = [t.replace(" ", "") for t in authors]
    # list_subjects = content.find_all('div', class_='list-subjects')

    # print(ids, "\n", titles, "\n", list_authors)
    # print(titles)
    # print(authors)

    items = []
    for i, paper in enumerate(zip(ids, titles, authors)):
        items.append({"ids": paper[0], "title": paper[1], "authors": paper[2]})

    print(items)
    '''send email'''
    content = 'Today arxiv2 has {} new papers.\n\n'.format(len(list_title))
    # content += 'Ensure your keywords is ' + str(key_words) + ' and ' + str(Key_words) + '(case=True). \n\n'
    content += '旅行者，今天也要加油哦！这是你今天的paper列表，请享用！！ \n\n'
    for i, paper_info in enumerate(items):
        content += '------------' + str(i + 1) + '------------\n' + paper_info["ids"] + '\n'
        content += 'Title:' + paper_info["title"] + '\n'
        content += 'https://arxiv.org/abs/' + paper_info["ids"] + '\n\n'

    title = time.strftime("%Y-%m-%d") + ' 亲爱的{}：你有 {} 篇文献还没看哦'.format(subscriber, len(list_title))

    print(content)
    # 发送邮箱
    send_email(title, content)


if __name__ == '__main__':
    main()
    time.sleep(1)
