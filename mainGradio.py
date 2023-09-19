import gradio as gr


def greet(name):
    return "Hello " + name + "!"


def print_btn(argg):
    print(argg, "++++")


with gr.Blocks() as demo:
    gr.Markdown("# 🕸️ arXiv 爬虫系统 🕷️")
    with gr.Tab("Setting"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# 文件存储位置设置")
                file_location = gr.Textbox(label="文件存储位置")
                save_file_button = gr.Button("保存文件存储位置设置", variant='primary')
            with gr.Column(scale=1):
                gr.Markdown("# SMTP邮箱设置")
                sender_email = gr.Textbox(label="sender_email")
                sender_email_password = gr.Textbox(label="sender_email_password")
                # abstract_input = gr.Textbox(label="abstract")

                save_email_button = gr.Button("保存邮箱设置", variant='primary')
    with gr.Tab("Index page"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# Search terms")
                title_input = gr.Textbox(label="title")
                author_input = gr.Textbox(label="author")
                abstract_input = gr.Textbox(label="abstract")

                gr.Markdown("# Subject")

                subject_checkbox = gr.CheckboxGroup(
                    ["Computer Science (cs)", "Electrical Engineering and Systems Science (eess)", "Mathematics (math)"],
                    info="Where are they from?")

                gr.Markdown("# Date")
                with gr.Row():
                    with gr.Column(scale=1):
                        date_from = gr.Textbox(label="From")
                    with gr.Column(scale=1):
                        date_to = gr.Textbox(label="To")
                btn12 = gr.Button("开始下载文献并发送到我的邮箱",variant='primary')
                btn12.click(print_btn, inputs=[subject_checkbox])
            with gr.Column(scale=1):
                with gr.Blocks():
                    with gr.Row():
                        inp = gr.Textbox(placeholder="What is your name?")
                        out = gr.Textbox()

if __name__ == "__main__":
    demo.launch()
