"""
@author Bcai
"""
import time
import butils


def subscribe_email():
    subscribers = butils.get_subscribers_list()
    for s in subscribers:
        cfg = butils.get_subscriber_config_dict(s)
        if cfg['newest-subscribed'] == 'y':
            pass


if __name__ == '__main__':
    subscribe_email()
    # time.sleep(60 * 60 * 24)
