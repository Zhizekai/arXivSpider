import yaml
import os
from urllib.parse import urlencode

"""
@author Bcai
"""
current_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(current_path, "config.yaml")
config_file = open(config_path, 'r', encoding="utf-8")
file_data = config_file.read()  # 读取file内容
config_file.close()
# print('sefs',config_file)
config_dict = yaml.safe_load(file_data)
# print(config_dict)
base_url = 'https://arxiv.org/search/advanced?advanced=&{}'
subject_dict = {
    'math': 'classification-mathematics',
    'cs': 'classification-computer_science'
}


# subscriber 订阅者 ， input_query_params 输入的查询参数
def get_url(subscriber: str = 'default', input_query_params=None) -> str:
    query_params = config_dict['default']['query-params'].copy()
    if not subscriber == 'default':
        query_params.update(config_dict['subscribers'][subscriber]['query-params'])
    if input_query_params:
        query_params = input_query_params
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
    if query_params['abstract']:
        query_params[f'terms-{term_i}-operator'] = 'AND'
        query_params[f'terms-{term_i}-term'] = query_params['abstract']
        query_params[f'terms-{term_i}-field'] = 'abstract'
        del query_params['abstract']
        term_i = term_i + 1

    # 设置搜索主题
    for s in query_params['subject']:
        query_params[subject_dict[s]] = 'y'
    del query_params['subject']

    # 删除空值
    for k in list(query_params.keys()):
        if not query_params[k]:
            del query_params[k]
    # print(query_params)
    return base_url.format(urlencode(query_params))


def get_email(subscriber):
    return config_dict['subscribers'][subscriber]['e-mail']
