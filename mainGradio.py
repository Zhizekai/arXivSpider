import gradio as gr


def greet(name):
    return "Hello " + name + "!"


def start_spider(*argg):
    print(argg)


# 保存设置的文件本地路径
def save_file_func(file_location_base):
    print(file_location_base)


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
    demo.launch()
