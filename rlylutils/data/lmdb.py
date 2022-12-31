# -*- coding:utf-8 -*-
# @Time    : 2022/12/20 23:11
# @Author  : Ray Lam YL


# import lmdb
#
#
# #a.encode("ascii")
# env = lmdb.open(path)
#
# txn=env.begin(write=False)
# #a=b'GOPRO_blur\\000271'
# a=a.encode()
# # a=b'GOPRO_blur\\000271'
# print(a)
# buf = txn.get(a)
# print('buf', buf)
#
# for key,value in txn.cursor():
#     print(key,value)
#
# env.close()