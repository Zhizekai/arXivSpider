"""
@author Bcai
"""
import json

import yaml
import os
from urllib.parse import urlencode
import requests
import time
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

current_path = os.path.abspath(".")
configs_path = os.path.join(current_path, 'config/')
config_subscriber_path_template = '../../uizekp/arXivSpider/config/config-{}.yaml'

caches_path = os.path.join(current_path, './cache/')

base_url = 'https://arxiv.org/search/advanced?advanced=&{}'
subject_dict = {
    'math': 'classification-computer_science',
    'cs': 'classification-mathematics'
}

config_dict = None


def get_config_dict() -> dict[str, any]:
    """
    获取全局配置文件
    :return:
    """
    global config_dict
    if config_dict:
        return config_dict.copy()

    config_file = open(configs_path + 'config.yaml', 'r', encoding="utf-8")
    file_data = config_file.read()  # 读取file内容
    config_file.close()
    # print('sefs',config_file)
    config_dict = yaml.safe_load(file_data)
    return config_dict.copy()


config_default_dict = get_config_dict()


def get_subscribers_list() -> list[str]:
    return [s.removeprefix('config-').removesuffix('.yaml') for s in os.listdir(configs_path) if not s == 'config.yaml']


def get_subscriber_config_dict(subscriber: str = None) -> dict[str, any]:
    if not str:
        return None
    config_path = config_subscriber_path_template.format(subscriber)

    if not os.path.exists(config_path):
        return None

    config_file = open(config_path, 'r', encoding="utf-8")
    file_data = config_file.read()  # 读取file内容
    config_file.close()
    config_dict = yaml.safe_load(file_data)
    return config_dict.copy()


def save_config(subscriber: str = None, config: dict[str, any] = None) -> dict[str, any]:
    if not subscriber or not config:
        return None

    config_path = config_subscriber_path_template.format(subscriber)
    with open(config_path, 'w', encoding="utf-8") as f:
        yaml.dump(config, f)
    return config


def get_subscriber_email(subscriber):
    return get_subscriber_config_dict(subscriber)['e-mail']


def del_subscriber_config(subscriber: str = None) -> bool:
    if not subscriber:
        return True
    config_path = config_subscriber_path_template.format(subscriber)
    if not os.path.exists(config_path):
        return True

    os.remove(config_path)
    return not os.path.exists(config_path)


def get_advanced_search_url(subscriber: str = 'default', start: int = 0,
                            query_params_dict: dict[str, any] = None) -> str:
    query_params = config_default_dict['query-params']
    if not subscriber == 'default':
        query_params.update(get_subscriber_config_dict(subscriber)['query-params'])
    if query_params_dict:
        query_params.update(query_params_dict)

    # 设置terms参数 （作者、类别、主题、摘要等）
    term_i = 0
    if 'all-fields' in query_params and query_params['all-fields']:
        query_params[f'terms-{term_i}-operator'] = 'AND'
        query_params[f'terms-{term_i}-term'] = query_params['all-fields']
        query_params[f'terms-{term_i}-field'] = 'all'
        del query_params['all-fields']
        term_i = term_i + 1

    if 'title' in query_params and query_params['title']:
        query_params[f'terms-{term_i}-operator'] = 'AND'
        query_params[f'terms-{term_i}-term'] = query_params['title']
        query_params[f'terms-{term_i}-field'] = 'title'
        del query_params['title']
        term_i = term_i + 1

    if 'authors' in query_params and query_params['authors']:
        query_params[f'terms-{term_i}-operator'] = 'AND'
        query_params[f'terms-{term_i}-term'] = query_params['authors']
        query_params[f'terms-{term_i}-field'] = 'author'
        del query_params['authors']
        term_i = term_i + 1
    if 'abstract' in query_params and query_params['abstract']:
        query_params[f'terms-{term_i}-operator'] = 'AND'
        query_params[f'terms-{term_i}-term'] = query_params['abstract']
        query_params[f'terms-{term_i}-field'] = 'abstract'
        del query_params['abstract']
        term_i = term_i + 1

    # 设置搜索主题
    for s in query_params['subject']:
        query_params[subject_dict[s]] = 'y'
    del query_params['subject']

    # 设置偏移
    query_params['start'] = start

    # 删除空值
    for k in list(query_params.keys()):
        if not query_params[k]:
            del query_params[k]
    # print(query_params)
    return base_url.format(urlencode(query_params))


def get_one_page(url):
    print(url)
    response = requests.get(url)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        print(response.status_code)
    print(response.status_code)
    if response.status_code == 200:
        return response.text
    return None


def get_paper_list(html):
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.ol

    list_ids = content.find_all('p', class_='list-title is-inline-block')
    ids = []
    pdf_urls = []
    for p in list_ids:
        alist = p.find_all('a')
        ids.append(alist[0].get_text())
        if len(alist) > 1:
            pdf_urls.append((alist[1].get('href')))

    list_title = content.find_all('p', class_='title is-5 mathjax')
    titles = [t.get_text().strip() for t in list_title]

    list_authors = content.find_all('p', class_='authors')
    authors = [t.get_text().replace("\n", "") for t in list_authors]
    authors = [t.replace(" ", "") for t in authors]
    # list_subjects = content.find_all('div', class_='list-subjects')

    items = []
    for i, paper in enumerate(zip(ids, titles, authors, pdf_urls)):
        items.append({"id": paper[0], "title": paper[1], "authors": paper[2][8:], "pdf_url": paper[3]})
    print(items)

    total = 100
    return items, total


# get_paper_list(get_one_page(get_advanced_search_url('u1')))

# cache
def get_subscriber_cache(subscriber: str = None) -> dict[str, any]:
    file_path = caches_path + f'cache-{subscriber}.json'
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    return json_data


def save_subscriber_cache(subscriber: str = None, data: dict[str, any] = None):
    file_path = caches_path + f'cache-{subscriber}.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)


def save_subscriber_newest_paper_id(subscriber: str, paper_id: str):
    cache = get_subscriber_cache(subscriber)
    cache['newest-paper-id'] = paper_id
    save_subscriber_cache(subscriber, cache)


def is_newest_paper(subscriber: str, paper_id: str) -> bool:
    """
    判断是不是最新发的论文；如果是第一次查询，则判定为最新发的论文
    """
    cache = get_subscriber_cache(subscriber)
    if not cache or 'newest-paper-id' not in cache:
        return True
    return cache['newest-paper-id'] != paper_id


# save_subscriber_cache('test', {'user': 'tst'})
# save_subscriber_newest_paper_id('test','arc')
# print(get_subscriber_cache('test'))
# print(is_newest_paper('test', 'arc'))


# email
def get_email_template(template_name: str = 'default'):
    return get_config_dict()['system']['e-mail']['template'][template_name]


def send_email(subscriber: str, receive_email: str, title, content, attach_path: str = None, file_name: str = None):
    """
    subscriber / receive_email二选一即可
    """
    sys_cfg = get_config_dict()['system']['e-mail']['send']
    # 发送者邮箱
    sender = sys_cfg['account']
    # 发送者的登陆用户名和密码
    user = sys_cfg['account']
    password = sys_cfg['password']  # dailyarxiv123
    # 发送者邮箱的SMTP服务器地址
    smtpserver = sys_cfg['smtp-server']
    # 接收者的邮箱地址
    if receive_email:
        receiver = receive_email  # receiver 可以是一个list
    else:
        receiver = get_subscriber_config_dict(subscriber)['e-mail']

    msg = MIMEMultipart('alternative')
    # 发送邮箱地址
    msg['From'] = sender
    # 收件箱地址
    msg['To'] = receiver
    # 主题
    msg['Subject'] = title

    # 填充消息
    part1 = MIMEText(content, 'plain', 'utf-8')
    msg.attach(part1)
    # 发送附件
    if attach_path:
        att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = f'attachment; filename="{file_name}"'
        msg.attach(att1)

    smtp = smtplib.SMTP()  # 实例化SMTP对象
    smtp.connect(smtpserver, 25)  # （缺省）默认端口是25 也可以根据服务器进行设定
    smtp.login(user, password)  # 登陆smtp服务器
    smtp.sendmail(sender, receiver, msg.as_string())  # 发送邮件 ，这里有三个参数
    '''
    login()方法用来登录SMTP服务器，sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文
    是一个str，as_string()把MIMEText对象变成str。
    '''
    smtp.quit()
# print(get_config_dict()['system']['e-mail']['template']['t1'].format('高','impact','lazi'))


if __name__ == '__main__':
    pass
