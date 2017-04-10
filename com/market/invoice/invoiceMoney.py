# -*- coding: utf-8 -*-

#黑名单金额计算
invoiceBlackMoney = 50
noInvoiceBlackMoney = 50
blackMoney = invoiceBlackMoney + noInvoiceBlackMoney

#正常商品金额计算
invoiceNomalMoney = 500
noInvoiceNomalMoney = 100
nomalMoney = invoiceNomalMoney + noInvoiceNomalMoney

#满减商品金额计算
cut = 100
invoiceActivityMoney = 200
noInvoiceActivityMoney = 300
activityMoney = invoiceActivityMoney + noInvoiceActivityMoney
resultInvoiceActivityMoney = invoiceActivityMoney - (cut/float(activityMoney))*invoiceActivityMoney

#现金券金额
couponCash = float(raw_input("现金券金额:"))

#判断使用的优惠券是否为品类优惠券
category = int(raw_input("是否使用了品类优惠券(1为是,2为否):"))
if(category == 1):
    isCoincidence = int(raw_input("满减活动和品类优惠券是否重合(1为是,2为否):"))
    if(isCoincidence == 1):
        coupon = 100
        categoryMoney = 600

        invoiceNoCoincidenceActivityMoney = 200
        noInvoiceNoCoincidenceActivityMoney = 100
        noCoincidenceActivityMoney = invoiceNoCoincidenceActivityMoney + noInvoiceNoCoincidenceActivityMoney

        coincidenceInvoiceMoney = 100
        coincidenceNoInvoiceMoney = 100
        coincidenceMoney = coincidenceInvoiceMoney + coincidenceNoInvoiceMoney

        noCoincidenceInvoiceMoney = 200
        noCoincidenceNoInvoiceMoney = 200
        noCoincidenceMoney = noCoincidenceInvoiceMoney + noCoincidenceNoInvoiceMoney

        #满减活动中未重复商品的可开票金额
        resultInvoiceActivityMoney = invoiceNoCoincidenceActivityMoney - ((invoiceNoCoincidenceActivityMoney/float(noCoincidenceActivityMoney))*cut*((activityMoney - coincidenceMoney)/float(activityMoney)))
        #满减与品类优惠券重复商品的可开票金额
        resultCoincidenceInvoiceMoney = coincidenceInvoiceMoney - (cut * (coincidenceMoney / float(activityMoney)) * (coincidenceInvoiceMoney / float(coincidenceMoney))) - (coupon*(coincidenceMoney/float(categoryMoney))*(coincidenceInvoiceMoney/float(coincidenceMoney)))
        #品类优惠中未重复商品的可开票金额
        resultNoCoincidenceMoney = noCoincidenceInvoiceMoney - (coupon *(noCoincidenceMoney/float(categoryMoney)) *(noCoincidenceInvoiceMoney/float(noCoincidenceMoney)))

        if (couponCash == 0):
            resultMoney = invoiceNomalMoney + invoiceBlackMoney + resultInvoiceActivityMoney + resultCoincidenceInvoiceMoney + resultNoCoincidenceMoney
            print "应付金额:%.2f"%(nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash )
            print "可开票金额:%.2f" % resultMoney
        else :
            print "应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash)
            flag = True
            while (flag):
                # 应付金额,nomalMoney + blackMoney + activityMoney + categoryMoney - couponCash
                money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
                if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney - coincidenceMoney - cut - coupon - couponCash)):
                    flag = False
                else:
                    flag = True
            resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney + resultCoincidenceInvoiceMoney + resultNoCoincidenceMoney) - ((couponCash / float(money + couponCash + coupon + cut - blackMoney)) * (invoiceNomalMoney + invoiceNoCoincidenceActivityMoney + coincidenceInvoiceMoney + noCoincidenceInvoiceMoney)) + invoiceBlackMoney
            print "可开票金额:%.2f" % resultMoney

    else:
        coupon = 100
        invoiceCategoryMoney = 200
        noInvoiceCategoryMoney = 300
        categoryMoney = invoiceCategoryMoney + noInvoiceCategoryMoney
        resultinvoiceCategoryMoney = invoiceCategoryMoney - (coupon/float(invoiceCategoryMoney + noInvoiceCategoryMoney)*invoiceCategoryMoney)
        if(couponCash == 0 ):
            resultMoney = invoiceNomalMoney + invoiceBlackMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney
            print "可开票金额:%.2f" %resultMoney
        else:
            print "通过计算得到的应付金额:%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney  - coupon - couponCash)
            flag = True
            while (flag):
                # 应付金额,nomalMoney + blackMoney + activityMoney + categoryMoney - couponCash
                money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
                if ("%.2f" % money == "%.2f" % (nomalMoney + blackMoney + activityMoney + categoryMoney  - coupon - couponCash)):
                    flag = False
                else:
                    flag = True

            resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney) - ((couponCash / float(money + couponCash - blackMoney)) * (invoiceNomalMoney + resultInvoiceActivityMoney + resultinvoiceCategoryMoney)) + invoiceBlackMoney
            print "可开票金额:%.2f" % resultMoney
else:
    #优惠券&现金券金额
    coupon = 100
    print "通过计算得到的应付金额:%.2f"%(nomalMoney + blackMoney + activityMoney - cut - coupon - couponCash)
    flag = True
    while(flag):
        # 应付金额,nomalMoney + blackMoney + activityMoney - coupon - cut
        money = float(raw_input("确认应付金额(可参考app中显示的应付金额):"))
        if("%.2f"%money == "%.2f"%(nomalMoney + blackMoney + activityMoney - cut - coupon - couponCash)):
            flag = False
        else:
            flag = True

    resultMoney = (invoiceNomalMoney + resultInvoiceActivityMoney) - (((coupon + couponCash) / float(money + coupon +couponCash - blackMoney)) * (invoiceNomalMoney + resultInvoiceActivityMoney)) + invoiceBlackMoney
    print "可开票金额:%.2f"%resultMoney

