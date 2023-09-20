"""
@author Bcai
"""
import time
import butils


def subscribe_email():
    subscribers = butils.get_subscribers_list()
    template = butils.get_email_template('newest-paper-reminder-1')
    for s in subscribers:
        cfg = butils.get_subscriber_config_dict(s)
        if cfg['newest-subscribed'] == 'y':
            papers, tmp = butils.get_paper_list(butils.get_one_page(butils.get_advanced_search_url(s)))
            if len(papers) > 0 and butils.is_newest_paper(s, papers[0]['id']):
                butils.save_subscriber_newest_paper_id(s, papers[0]['id'])  # 更新最新文章的id
                # 发送邮件
                content = template.format(papers[0]['title'], papers[0]['authors'], papers[0]['pdf_url'])
                butils.send_email(s, cfg['e-mail'], '新文章提醒',content)


if __name__ == '__main__':
    subscribe_email()
    # butils.send_email(None, '1364761092@qq.com', 'asdas','asdadasdasd')
    # time.sleep(60 * 60 * 24)
