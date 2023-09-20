import gradio as gr
import url as _url
from butils import get_paper_list,get_one_page


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
    # print(query_params)
    url = _url.get_url('bcai', query_params)
    html = get_one_page(url)
    print(
        get_paper_list(html)
    )


# 保存设置的文件本地路径
def save_file_func(*kwargs):
    print(kwargs)


# 保存SMTP邮箱设置
def save_email_func(*kwargs):
    print(kwargs[0])
    print(kwargs[1])


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
                btn12.click(start_spider,
                            inputs=[title_input, author_input, abstract_input, subject_checkbox, date_from, date_to])

            with gr.Column(scale=1):
                gr.Markdown("# 文件存储位置设置")
                file_location = gr.Textbox(value='D:\src', label="文件存储位置")
                save_file_button = gr.Button("保存文件存储位置设置", variant='primary')
                save_file_button.click(save_file_func, inputs=[file_location])

                gr.Markdown("# 下载设置")
                file_num = gr.Textbox(value='10', label="下载文章个数")
                save_download_setting_button = gr.Button("保存下载设置", variant='primary')
                save_download_setting_button.click(save_file_func, inputs=[file_num])
    with gr.Tab("订阅最新论文信息"):
        with gr.Row():
            with gr.Column(scale=1):
                # gr.Markdown("# Search terms")
                # title_input = gr.Textbox(label="title")
                # author_input = gr.Textbox(label="author")
                # abstract_input = gr.Textbox(label="abstract")

                gr.Markdown("# Subject")

                subject_checkbox = gr.CheckboxGroup(
                    ["Computer Science (cs)", "Economics (econ)", "Electrical Engineering and Systems Science (eess)",
                     "Mathematics (math)", "Quantitative Biology (q-bio)", "Quantitative Finance (q-fin)",
                     "Statistics (stat)"],
                    info="你想要搜什么类型的")

                gr.Markdown("# Date")
                with gr.Row():
                    with gr.Column(scale=1):
                        date_from = gr.Textbox(label="From")
                    with gr.Column(scale=1):
                        date_to = gr.Textbox(label="To")
                btn12 = gr.Button("开始订阅", variant='primary')
                btn12.click(start_spider,
                            inputs=[title_input, author_input, abstract_input, subject_checkbox, date_from, date_to])
            with gr.Column(scale=1):
                gr.Markdown("# SMTP邮箱设置")
                sender_email = gr.Textbox(value="1310248516@qq.com", label="sender_email")
                sender_email_password = gr.Textbox(label="sender_email_password")
                # abstract_input = gr.Textbox(label="abstract")

                save_email_button = gr.Button("保存邮箱设置", variant='primary')
                save_email_button.click(save_email_func, inputs=[sender_email, sender_email_password])

                with gr.Blocks():
                    with gr.Row():
                        inp = gr.Textbox(placeholder="What is your name?")
                        out = gr.Textbox()

if __name__ == "__main__":
    demo.queue().launch()
