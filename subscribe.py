"""
@author Bcai
"""
import datetime

import butils
from apscheduler.schedulers.blocking import BlockingScheduler


def subscribe_email():
    print(f'订阅最新文章提醒脚本-start：{datetime.datetime.now()}')
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
                butils.send_email(s, cfg['e-mail'], '新文章提醒', content)
                print(f'向{s}: {cfg["e-mail"]}发送了新邮件：\n{content}\n')
    print(f'订阅最新文章提醒脚本-end：{datetime.datetime.now()}')


if __name__ == '__main__':
    # 调度框架每周一和周四早上7:00执行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(subscribe_email, 'cron', max_instances=1, day_of_week='mon,thu', hour=7, minute=0)
    scheduler.start()
