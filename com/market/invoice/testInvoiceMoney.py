# -*- coding: utf-8 -*-

# 黑名单金额计算
invoiceBlackMoney = 25
noInvoiceBlackMoney = 0
blackMoney = invoiceBlackMoney + noInvoiceBlackMoney

# 正常商品金额计算
invoiceNomalMoney = 3026.6
noInvoiceNomalMoney = 60.22
nomalMoney = invoiceNomalMoney + noInvoiceNomalMoney

# 满减商品金额计算
cut = 10
invoiceActivityMoney = 300
noInvoiceActivityMoney = 33
activityMoney = invoiceActivityMoney + noInvoiceActivityMoney
resultInvoiceActivityMoney = invoiceActivityMoney - (cut / float(activityMoney)) * invoiceActivityMoney

# 满减商品金额计算2
cut2 = 5
invoiceActivityMoney2 = 164
noInvoiceActivityMoney2 = 200
activityMoney2 = invoiceActivityMoney2 + noInvoiceActivityMoney2
resultInvoiceActivityMoney2 = invoiceActivityMoney2 - (cut2 / float(activityMoney2)) * invoiceActivityMoney2

# 现金券金额
couponCash = float(raw_input("现金券金额:"))

class testInvoiceMoney:
    #无满减活动无黑名单
    def nomalCase(self):
        # 优惠券
        coupon = 100
        print "通过计算得到的应付金额:%.2f" % (nomalMoney - coupon - couponCash)
        flag = True
        while (flag):
            # 应付金额,nomalMoney + blackMoney + activityMoney - coupon - cut
            money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
            if ("%.2f" % money == "%.2f" % (nomalMoney - coupon - couponCash)):
                flag = False
            else:
                flag = True
        resultMoney = invoiceNomalMoney - (((coupon + couponCash) / float(money + coupon + couponCash)) * invoiceNomalMoney)
        print "可开票金额:%.2f" % resultMoney

    #无满减有黑名单
    def blackCase(self):
        # 优惠券
        coupon = 100
        print "通过计算得到的应付金额:%.2f" % (nomalMoney + blackMoney - coupon - couponCash)
        flag = True
        while (flag):
            # 应付金额,nomalMoney + blackMoney + activityMoney - coupon - couponCash
            money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
            if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney - coupon - couponCash)):
                flag = False
            else:
                flag = True
        resultMoney = invoiceNomalMoney - (((coupon + couponCash) / float(money + coupon + couponCash - blackMoney)) * invoiceNomalMoney ) + invoiceBlackMoney
        print "可开票金额:%.2f" % resultMoney

    #有满减有黑名单
    def activityCase(self):
        # 优惠券
        coupon = 10
        print "通过计算得到的应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney - cut - coupon - couponCash)
        flag = True
        while (flag):
            # 应付金额,nomalMoney + blackMoney + activityMoney - coupon - cut - couponCash
            money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
            if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney - cut - coupon - couponCash)):
                flag = False
            else:
                flag = True
        #普通商品可开票金额
        resultInvoiceNomalMoney = invoiceNomalMoney -  ((coupon + couponCash) / float(money + coupon + couponCash + cut - blackMoney))*invoiceNomalMoney
        #参与满减商品可开票金额
        resultCouponInvoiceActivityMoney = resultInvoiceActivityMoney - ((coupon + couponCash) / float(money + coupon + couponCash + cut - blackMoney))*invoiceActivityMoney
        #最终可开票金额
        resultMoney = resultInvoiceNomalMoney + resultCouponInvoiceActivityMoney + invoiceBlackMoney
        '''
        resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney) - (
        ((coupon + couponCash) / float(money + coupon + couponCash + cut - blackMoney)) * (
        invoiceNomalMoney + invoiceActivityMoney)) + invoiceBlackMoney
        '''
        print "可开票金额:%.2f" % resultMoney

    #有两个满减活动有黑名单
    def twoActivitiesCase(self):
        # 优惠券
        coupon = 20
        print "通过计算得到的应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney - cut + activityMoney2 - cut2 - coupon - couponCash)
        flag = True
        while (flag):
            # 应付金额,nomalMoney + blackMoney + activityMoney - coupon - cut - couponCash
            money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
            if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney - cut + activityMoney2 - cut2 - coupon - couponCash)):
                flag = False
            else:
                flag = True
        # 普通商品可开票金额
        resultInvoiceNomalMoney = invoiceNomalMoney - ((coupon + couponCash) / float(money + coupon + couponCash + cut + cut2 - blackMoney)) * invoiceNomalMoney
        # 参与满减1商品可开票金额
        resultCouponInvoiceActivityMoney = resultInvoiceActivityMoney - ((coupon + couponCash) / float(money + coupon + couponCash + cut + cut2 - blackMoney)) * invoiceActivityMoney
        # 参与满减2商品可开票金额
        resultCouponInvoiceActivityMoney2 = resultInvoiceActivityMoney2 - ((coupon + couponCash) / float(money + coupon + couponCash + cut + cut2 - blackMoney)) * invoiceActivityMoney2
        # 最终可开票金额
        resultMoney = resultInvoiceNomalMoney + resultCouponInvoiceActivityMoney + resultCouponInvoiceActivityMoney2 + invoiceBlackMoney
        '''
        resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney + resultInvoiceActivityMoney2) - (((coupon + couponCash) / float(money + coupon + couponCash + cut + cut2 - blackMoney)) * (invoiceNomalMoney + invoiceActivityMoney + invoiceActivityMoney2)) + invoiceBlackMoney
        '''
        print "可开票金额:%.2f" % resultMoney

    #有满减有黑名单有品类优惠券,但满减商品和品类优惠券商品没重合
    def noCoincidenceCase(self):
        coupon = 100
        invoiceCategoryMoney = 200
        noInvoiceCategoryMoney = 300
        categoryMoney = invoiceCategoryMoney + noInvoiceCategoryMoney
        resultinvoiceCategoryMoney = invoiceCategoryMoney - (
        coupon / float(invoiceCategoryMoney + noInvoiceCategoryMoney) * invoiceCategoryMoney)
        if (couponCash == 0):
            resultMoney = invoiceNomalMoney + invoiceBlackMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney
            print "可开票金额:%.2f" % resultMoney
        else:
            print "通过计算得到的应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coupon - couponCash)
            flag = True
            while (flag):
                # 应付金额,nomalMoney + blackMoney + activityMoney + categoryMoney - couponCash
                money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
                if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coupon - couponCash)):
                    flag = False
                else:
                    flag = True
            resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney) - (
            (couponCash / float(money + couponCash - blackMoney)) * (
            invoiceNomalMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney)) + invoiceBlackMoney
            print "可开票金额:%.2f" % resultMoney

    #有满减有黑名单有品类优惠券,且满减商品和品类优惠券商品有重合
    def coincidenceCase(self):
        coupon = 100
        #品类商品的总金额
        categoryMoney = 600
        #参与满减且没有和品类优惠券重叠的商品金额
        invoiceNoCoincidenceActivityMoney = 200
        noInvoiceNoCoincidenceActivityMoney = 100
        noCoincidenceActivityMoney = invoiceNoCoincidenceActivityMoney + noInvoiceNoCoincidenceActivityMoney
        #满减商品和品类优惠券商品重复的金额
        coincidenceInvoiceMoney = 100
        coincidenceNoInvoiceMoney = 100
        coincidenceMoney = coincidenceInvoiceMoney + coincidenceNoInvoiceMoney
        #参与品类优惠券且没有和满减重叠的商品金额
        noCoincidenceInvoiceMoney = 200
        noCoincidenceNoInvoiceMoney = 200
        noCoincidenceMoney = noCoincidenceInvoiceMoney + noCoincidenceNoInvoiceMoney
        # 满减活动中未重复商品的可开票金额
        resultInvoiceActivityMoney = invoiceNoCoincidenceActivityMoney - (
        (invoiceNoCoincidenceActivityMoney / float(noCoincidenceActivityMoney)) * cut * (
        (activityMoney - coincidenceMoney) / float(activityMoney)))
        # 满减与品类优惠券重复商品的可开票金额
        resultCoincidenceInvoiceMoney = coincidenceInvoiceMoney - (
        cut * (coincidenceMoney / float(activityMoney)) * (coincidenceInvoiceMoney / float(coincidenceMoney))) - (
                                        coupon * (coincidenceMoney / float(categoryMoney)) * (
                                        coincidenceInvoiceMoney / float(coincidenceMoney)))
        # 品类优惠中未重复商品的可开票金额
        resultNoCoincidenceMoney = noCoincidenceInvoiceMoney - (
        coupon * (noCoincidenceMoney / float(categoryMoney)) * (noCoincidenceInvoiceMoney / float(noCoincidenceMoney)))

        if (couponCash == 0):
            resultMoney = invoiceNomalMoney + invoiceBlackMoney + resultInvoiceActivityMoney + resultCoincidenceInvoiceMoney + resultNoCoincidenceMoney
            print "应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash)
            print "可开票金额:%.2f" % resultMoney
        else:
            print "应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash)
            flag = True
            while (flag):
                # 应付金额,nomalMoney + blackMoney + activityMoney + categoryMoney - couponCash
                money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
                if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash)):
                    flag = False
                else:
                    flag = True
            resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney + resultCoincidenceInvoiceMoney + resultNoCoincidenceMoney) - (
                          (couponCash / float(money + couponCash + coupon + cut - blackMoney)) * (
                          invoiceNomalMoney + invoiceNoCoincidenceActivityMoney + coincidenceInvoiceMoney + noCoincidenceInvoiceMoney)) + invoiceBlackMoney
            print "可开票金额:%.2f" % resultMoney

case = testInvoiceMoney()
#case.activityCase()
case.twoActivitiesCase()
#case.nomalCase()
#case.blackCase()
#有现金券和无现金券分别算
#case.noCoincidenceCase()
#有现金券和无现金券分别算
#case.coincidenceCase()
