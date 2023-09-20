"""
@author Bcai
"""
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

base_url = 'https://arxiv.org/search/advanced?advanced=&{}'
subject_dict = {
    'math': 'classification-computer_science',
    'cs': 'classification-mathematics'
}


def get_config_dict() -> dict[str, any]:
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
        if alist[1].get('href'):
            pdf_urls.append((alist[1].get('href')))

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
    for i, paper in enumerate(zip(ids, titles, authors, pdf_urls)):
        items.append({"ids": paper[0], "title": paper[1], "authors": paper[2][8:], "pdf_url": paper[3]})
    print(items)

    total = 100
    return items, total


# get_paper_list(get_one_page(get_advanced_search_url('u1')))

# cache
def save_cache_():
    pass


if __name__ == '__main__':
    pass
