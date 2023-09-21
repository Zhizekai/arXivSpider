import gradio as gr
import url as _url
import requests
from butils import get_paper_list, get_one_page, save_config

import io
from multiprocessing import pool
import time

save_path = 'D:\\src\\'  # 保存文件的路径
global_file_num = '10'  # 下载文件个数
subscribe_person = 'bcai'  # 订阅人名称


def greet(name):
    return "Hello " + name + "!"


# 开始爬虫
def start_spider(*argg):
    query_params = {'title': argg[0], 'authors': argg[1], 'abstract': argg[2], 'subject': []}

    def square(x):
        subject_dict = {
            'Mathematics (math)': 'math',
            'Computer Science (cs)': 'cs'
        }
        return subject_dict[x]

    query_params['subject'] = query_params['subject'] + list(map(square, argg[3]))

    query_params['date-from_date'] = argg[4]
    query_params['date-to_date'] = argg[5]
    # aa = []
    # for i in range(10):
    #
    #     aa.append(["loading", " 下载成功'+str(i)"])
    #     print(aa)
    #     time.sleep(2)
    #     yield aa
    url = _url.get_url('bcai', query_params)
    html = get_one_page(url)
    result_list, _ = get_paper_list(html)

    result_msg = []

    # p = pool.Pool()

    def download_pdf(save_path, pdf_name, pdf_url):
        send_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}

        # 代理设置
        proxies = {
            "http": "http://localhost:7890",
            "https": "http://localhost:7890",
        }
        response = requests.get(pdf_url, headers=send_headers, allow_redirects=True, proxies=proxies)
        bytes_io = io.BytesIO(response.content)
        with open(save_path + "%s.PDF" % pdf_name, mode='wb') as f:
            f.write(bytes_io.getvalue())
            print('%s.PDF,下载成功！' % (pdf_name))

    for index, item in enumerate(result_list):
        if index == int(global_file_num):
            break

        # p.apply_async(download_pdf, args=(save_path, item['title'], item['pdf_url']))
        download_pdf(save_path=save_path, pdf_name=item['title'], pdf_url=item['pdf_url'])
        result_msg.append(["loading。。。。。", item['title'] + "下载成功 "])
        yield result_msg

    # p.close()
    # p.join()


# 保存设置的文件本地路径
def save_file_func(*kwargs):
    global save_path
    global global_file_num
    save_path = kwargs[0]
    global_file_num = kwargs[1]


# 保存SMTP邮箱设置
def save_email_func(*kwargs):
    print(kwargs[0])
    print(kwargs[1])
    print(kwargs[2])
    email_subscribe_setting_dict = {
        "e-mail": kwargs[0]
    }
    save_config(subscribe_person, email_subscribe_setting_dict)


# 开始订阅，保存订阅设置，订阅进程单独开启，到时间会自动读取订阅信息进行发送邮件
def start_subscribe(*kwargs):
    print(kwargs)


with gr.Blocks() as demo:
    gr.Markdown("# 🕸️ arXiv 爬虫系统 🕷️")
    with gr.Tab("下载文献"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# Search terms")
                title_input = gr.Textbox(label="title")
                author_input = gr.Textbox(label="author")
                abstract_input = gr.Textbox(label="abstract")

                gr.Markdown("# Subject")

                subject_checkbox = gr.CheckboxGroup(
                    ["Computer Science (cs)", "Economics (econ)", "Electrical Engineering and Systems Science (eess)",
                     "Mathematics (math)", "Quantitative Biology (q-bio)", "Quantitative Finance (q-fin)",
                     "Statistics (stat)"],
                    info="你想要搜什么类型的")

                gr.Markdown("# Date")
                with gr.Row():
                    with gr.Column(scale=1):
                        date_from = gr.Textbox(value="2020-03-18", label="From")
                    with gr.Column(scale=1):
                        date_to = gr.Textbox(value="2022-03-18", label="To")

                btn12 = gr.Button("开始下载论文", variant='primary')

            with gr.Column(scale=1):
                gr.Markdown("# 文件存储位置设置")
                file_location = gr.Textbox(value=save_path, label="文件存储位置")
                # save_file_button = gr.Button("保存文件存储位置设置", variant='primary')
                # save_file_button.click(save_file_func, inputs=[file_location])

                gr.Markdown("# 下载设置")
                file_num = gr.Textbox(value=global_file_num, label="下载文章个数")
                save_download_setting_button = gr.Button("保存下载设置", variant='primary')
                save_download_setting_button.click(save_file_func, inputs=[file_location, file_num])

                chatbot = gr.Chatbot()

                btn12.click(start_spider,
                            inputs=[title_input, author_input, abstract_input, subject_checkbox, date_from, date_to],
                            outputs=[chatbot]
                            )
    with gr.Tab("订阅最新论文信息"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# subscribe terms")
                title_input = gr.Textbox(label="title")
                author_input = gr.Textbox(label="author")
                abstract_input = gr.Textbox(label="abstract")

                gr.Markdown("# Subject")
                subject_checkbox = gr.CheckboxGroup(
                    ["Computer Science (cs)", "Economics (econ)", "Electrical Engineering and Systems Science (eess)",
                     "Mathematics (math)", "Quantitative Biology (q-bio)", "Quantitative Finance (q-fin)",
                     "Statistics (stat)"],
                    info="你想要订阅什么类型的")

                start_subscribe_button = gr.Button("开始订阅", variant='primary')
                start_subscribe_button.click(start_subscribe,
                                             inputs=[title_input, author_input, abstract_input, subject_checkbox])
            with gr.Column(scale=1):
                gr.Markdown("订阅人设置")
                subscribe_person_input = gr.Textbox(value=subscribe_person, label="订阅人")

                gr.Markdown("# SMTP邮箱设置")
                sender_email_input = gr.Textbox(value="1310248516@qq.com", label="sender_email")
                sender_email_password_input = gr.Textbox(label="sender_email_password")
                # abstract_input = gr.Textbox(label="abstract")

                save_email_button = gr.Button("保存邮箱设置", variant='primary')
                save_email_button.click(save_email_func, inputs=[sender_email_input, sender_email_password_input,
                                                                 subscribe_person_input])

if __name__ == "__main__":
    demo.queue()
    demo.launch()
