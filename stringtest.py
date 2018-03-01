#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20180204
@author:wyl QQ635864540
python version 2.7
'''
__author__ = 'wyl QQ635864540'

import string

str = '123456789'
print str
index = str.find('9')
if index != -1:
	str = str.replace('9','')
print str
i = 0
i += 1
print i

str = '12345676'
index = str.find('8')
print index
for i in range(0,len(str)):
	print str[i]
	
def MakeArray(array):
	results = []
	length = len(array)
	for elements in array:
		if len(results) == 0:
			for element in elements:
				results.append(element)
		else:
			tempArray = []
			for res in results:
				for element in elements:
					if res.find(element) == -1:
						tempArray.append(res + element)
			results = tempArray
	return results
	
arrays = ['123','27','789']
results = MakeArray(arrays)
print results