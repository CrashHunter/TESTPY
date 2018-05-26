#!/usr/bin/env python
# -*- coding: utf-8 -*-

# def test():
#     time = 30
#     MMN = 15
#     N = time / MMN
#
#     print N
#     nexttime = MMN * (N + 2) % 60
#     print(nexttime)
#
#
# test()


import datetime
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

# def viewBar(i):
#     output = sys.stdout
#     for count in range(0, i + 1):
#         now = datetime.datetime.now()
#         second = 0.1
#         sleep(second)
#         # output.write('\r running...' + str(now.second))
#         print('\r start')
#     # output.flush()
#     print(1 / float(3))
#
#
# viewBar(100)
# for i in range(5):
#     sys.stdout.write(' ' * 10 + '\r')
#     sys.stdout.flush()
#     sys.stdout.write(str(i) * (5 - i) + '\r')
#     sys.stdout.flush()
#     time.sleep(1)
# from datetime import datetime

output = sys.stdout


def job():
    now = datetime.datetime.now()

    # print "\r Hello, Gay! ", now.second,
    # sys.stdout.flush()
    output.write("\r time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    # sys.stdout.flush()


# 定义BlockingScheduler
sched = BlockingScheduler()
# sched = BackgroundScheduler()
sched.add_job(job, 'interval', seconds=1)
# sched.add_job(job2, 'interval', seconds=2)
sched.start()

# now = datetime.datetime.now()
# print("ssss")
# print(" time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))

# import curses
# pad = curses.newpad(100, 100)
# #  These loops fill the pad with letters; this is
# # explained in the next section
# for y in range(0, 100):
#     for x in range(0, 100):
#         try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
#         except curses.error: pass
#
# #  Displays a section of the pad in the middle of the screen
# pad.refresh( 0,0, 5,5, 20,75)
#
