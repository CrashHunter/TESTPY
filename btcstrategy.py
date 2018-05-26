#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from HuobiService import *

# logging.basicConfig()

open = close = high = low = cur = 0

# 建仓点位
openPosition = 0
# 规则触发次数
actionNum = 0
# 规则成功次数
actionSuc = 0

# 成功累计盈利
totalProfit = 0

minus = -1
action = 'buy'

# 是否建仓
order = False

# 波动率
checkPointRate = 0.0005
# 几分钟K线
KType = '5min'
# 几分钟K线
MMN = 5
# 平仓时间
nextMinTime = 0
# 交易对
pair = 'btcusdt'
# 下单量
value = '0.0011'
import sys

output = sys.stdout


def sellAction(price):
    print ' *************  sellAction:' + price
    # send_order(value, '', pair, 'sell-limit', price)


def buyAciton(price):
    print ' *************  buyAction:' + price
    # send_order(value, '', pair, 'buy-limit', price)


def waitCheckPoint():
    global open
    global cur
    global high
    global low
    global close

    global minus
    global action
    global order
    global nextMinTime

    kline = get_kline(pair, KType, '1')
    # print(kline)

    open = kline['data'][0]['open']
    high = kline['data'][0]['high']
    low = kline['data'][0]['low']
    cur = kline['data'][0]['close']

    checkpoint = open * checkPointRate

    if high - open > open - low:
        action = 'sell'
        minus = cur - low
    elif high - open <= open - low:
        action = 'buy'
        minus = high - cur

    now = datetime.datetime.now()

    # print(" time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    sucRate = 0
    if actionSuc != 0:
        sucRate = actionSuc / float(actionNum)

    # output.write('\r cur:' + str(cur)
    #              + " minus:" + str(minus)
    #              + " CP:" + str(checkpoint)
    #              + " ACT:" + str(action)
    #              + " O:" + str(open)
    #              + " H:" + str(high)
    #              + " L:" + str(low)
    #              + " ACTNUM:" + str(actionNum)
    #              + " sRate:" + str(sucRate)
    #              + " tProfit:" + str(totalProfit)
    #              + " time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    # sys.stdout.flush()
    if minus >= checkpoint:
        order = True
        nextMinTime = MMN * (now.minute / MMN + 2) % 60
        print(' ++++++++++++   get checkpoint: cur:' + str(cur)
              + " minus:" + str(minus)
              + " CP:" + str(checkpoint)
              + " CPR:" + str(checkPointRate)
              + " ACT:" + str(action)
              + " O:" + str(open)
              + " H:" + str(high)
              + " L:" + str(low)
              + " ACTNUM:" + str(actionNum)
              + " sRate:" + str(sucRate)
              + " tProfit:" + str(totalProfit)
              + " time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
              + " nextMinTime:" + str(nextMinTime))

        job2()
        # print ('\n ##############   get checkpoint' + 'minus:' + str(minus)
        #        + " checkpoint:" + str(checkpoint)
        #        + " action:" + str(action)
        #        + " open:" + str(open)
        #        + " high:" + str(high)
        #        + " low:" + str(low)
        #        + " actionNum:" + str(actionNum)
        #        + " time:" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        #        + " nextMinTime:" + str(nextMinTime))
        sys.stdout.flush()


def job():
    global close
    global order
    global actionSuc
    global totalProfit

    now = datetime.datetime.now()
    # print now.year, now.month, now.day, now.hour, now.minute, now.second

    if order:
        # output.write(
        #     '\r openPosition：' + str(openPosition) + " response... wait for:" + str(nextMinTime) + " " + str(
        #         now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        # sys.stdout.flush()
        # print "openPosition：", openPosition, " response... wait for:", nextMinTime, now.year, now.month, now.day, now.hour, now.minute, now.second
        if now.second <= 10 and now.minute == nextMinTime:
            print " ----------  time to reaction"
            kline = get_kline(pair, KType, '1')
            close = kline['data'][0]['close']
            if action == 'buy':
                if cur < close:
                    actionSuc += 1
                    totalProfit += (close - openPosition) * float(value) - 0.002 * close * float(
                        value) - 0.002 * openPosition * float(value)
                    print " 平仓卖", " openPosition：", openPosition, " closePosition:", close
                    sellAction(str(close))
                else:
                    print ' 低买高卖失败', " openPosition：", openPosition, " closePosition:", close
            elif action == 'sell':
                if cur > close:
                    actionSuc += 1
                    totalProfit += (openPosition - close) * float(value) - 0.002 * close * float(
                        value) - 0.002 * openPosition * float(value)
                    print " 平仓买", " openPosition：", openPosition, " closePosition:", close
                    buyAciton(str(close))
                else:
                    print ' 高卖低买失败', " openPosition：", openPosition, " closePosition:", close

            order = False
            sys.stdout.flush()
        return
    else:
        waitCheckPoint()


def job2():
    global actionNum
    global openPosition
    openPosition = cur
    actionNum += 1
    if action == 'buy':
        buyAciton(str(cur))
    elif action == 'sell':
        sellAction(str(cur))


print('\n start')
# 定义BlockingScheduler
sched = BlockingScheduler()
# sched = BackgroundScheduler()
sched.add_job(job, 'interval', seconds=1)
# sched.add_job(job2, 'interval', seconds=2)
sched.start()
