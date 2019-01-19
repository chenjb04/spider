# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/1/16 18:59'
import random


def get_user_agent():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = ['(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)', '(Macintosh; Intel Mac OS X 10_12_6)']

    chrom_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36', '(KHTML, like Gecko)', chrom_version, 'Safari/537.36'])
    return ua


if __name__ == '__main__':
    print(get_user_agent())