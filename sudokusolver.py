#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20180301
@author:wyl QQ635864540
python version 2.7
'''
__author__ = 'wyl QQ635864540'

import os
import time

class ClsSudokuSolver:
	def __init__(self):
		self.filename = 'puzzle.txt'
		self.maxlength = 9
		self.debugtype = False
		
	def Solver(self):
		begintime = time.strftime('%Y-%m-%d %H:%M:%S ')
		print begintime
		print '========================='
		#read puzzle from file
		with open(self.filename, 'r') as f:
			results = f.readlines()
		f.close()
		
		tempArray = []
		for i in range(0,9):
			line = results[i].strip()
			tempArray.append(line)
		results = tempArray
		
		#find all reversed number 
		allreversed = [['']*9 for i in range(9)]
		print allreversed
		i = 0
		j = 0
		while i<9:
			j = 0
			while j<9:
				allreversed[i][j] = '123456789'
				j = j + 1
			i = i + 1
		linenum = 0
		colnum = 0
		for line in results:
			line = line.strip()
			print line
			colnum = 0
			while colnum < 9:
				if line[colnum] != '.':
					allreversed[linenum][colnum] = line[colnum]
					innerlinenum = linenum
					innercolnum = 0
					while innercolnum < 9:
						if innercolnum != colnum:
							allreversed[innerlinenum][innercolnum] = allreversed[innerlinenum][innercolnum].replace(line[colnum],'')
						innercolnum = innercolnum + 1
					innercolnum = colnum
					innerlinenum = 0
					while innerlinenum < 9:
						if innerlinenum != linenum:
							allreversed[innerlinenum][innercolnum] = allreversed[innerlinenum][innercolnum].replace(line[colnum],'')
						innerlinenum = innerlinenum + 1
						
					#every 3*3 sudoku should be from 1 to 9
					innerlinenum = 0
					innercolnum = 0
					currentloc = linenum/3*3 + colnum/3
					#print currentloc
					while innerlinenum < 9:
						innercolnum = 0
						while innercolnum < 9:
							if linenum!=innerlinenum or colnum!=innercolnum:
								if innerlinenum/3*3 + innercolnum/3==currentloc:
									allreversed[innerlinenum][innercolnum] = allreversed[innerlinenum][innercolnum].replace(line[colnum],'')									
							innercolnum += 1
						innerlinenum += 1
				colnum = colnum + 1
			linenum = linenum + 1
			if linenum >= 9:
				break
			
		print ''
		print ''
		print 'After calculate:'
		i = 0
		while i < 9:
			print allreversed[i]
			i = i + 1
			
		print ''
		print ''
		print 'Calc results:'
		print results
		print allreversed
		print '========================='
		self.CalcResult(results, allreversed)
		print '========================='
		endtime = time.strftime('%Y-%m-%d %H:%M:%S ')
		print begintime
		print endtime
		
	def CalcResult(self, results, allreversed):
		while True:
			bFound = True
			linenum = 0
			for line in results:
				line = line.strip()
				colnum = 0
				innerline = ''
				while colnum < 9:
					if line[colnum] == '.':
						if len(allreversed[linenum][colnum]) == 1:
							ele = allreversed[linenum][colnum]
							innerline += ele
							results[linenum] = innerline + results[linenum][colnum+1:]
							line = results[linenum]
							#current line, all columns should remove this element
							innercolnum = 0
							while innercolnum < 9:
								if innercolnum != colnum and len(allreversed[linenum][innercolnum]) > 1:
									allreversed[linenum][innercolnum] = allreversed[linenum][innercolnum].replace(ele,'')
									bFound = False
								innercolnum += 1
							#current col, all lines should remove this element
							innerlinenum = 0
							while innerlinenum < 9:
								if innerlinenum != linenum and len(allreversed[innerlinenum][colnum]) > 1:
									allreversed[innerlinenum][colnum] = allreversed[innerlinenum][colnum].replace(ele,'')
									bFound = False
								innerlinenum += 1
							break
						else:
							innerline += line[colnum]
					else:
						element = line[colnum]
						innerline += element
						innerlinenum = 0
						innercolnum = 0
						currentloc = linenum/3*3 + colnum/3
						#print currentloc
						while innerlinenum < 9:
							innercolnum = 0
							while innercolnum < 9:
								if linenum!=innerlinenum or colnum!=innercolnum:
									if innerlinenum/3*3 + innercolnum/3==currentloc:
										#if len(allreversed[innerlinenum][innercolnum]) == 1:
										#	break
										if allreversed[innerlinenum][innercolnum].find(element) != -1:
											bFound = False
											allreversed[innerlinenum][innercolnum] = allreversed[innerlinenum][innercolnum].replace(element,'')									
								innercolnum += 1
							innerlinenum += 1
					colnum += 1
				linenum += 1
				if linenum >= 9:
					break
			if self.debugtype:
				print results
				print allreversed
			#bRecalcResult = False
			#linenum2 = 0
			#for linearray in allreversed:
			#	colnum2 = 0
			#	alleles = ''
			#	while colnum2 < 9:
			#		if len(linearray[colnum2]) >= 2:
			#			alleles += linearray[colnum2]
			#		colnum2 += 1
			#	for i in range(0,len(alleles)):
			#		if alleles.count(alleles[i]) == 1:
			#			#print alleles[i]
			#			colnum2 = 0
			#			while colnum2 < 9:
			#				if allreversed[linenum2][colnum2].find(alleles[i]) != -1:
			#					allreversed[linenum2][colnum2] = alleles[i]
			#					bRecalcResult = True
			#				colnum2 += 1							
			#	linenum2 += 1
			#	if linenum2 >= 9:
			#		break
			#if bRecalcResult:
			#	self.CalcResult(results, allreversed)
			if bFound:
				break
		print results
		print allreversed
		print 'Final Results:'
		results = self.FinalResult(results, allreversed)
		if self.IsValidSudoku(results):
			print 'Valid'
			for line in results:
				print line.strip()
		else:
			print 'Invalid'
			print results
					
	def FinalResult(self, results, allreversed):
		#get all reversed numbers to create new array for every line
		randomarray = [[] for i in range(0,9)]
		for i in range(0,9):
			array = self.MakeArray(allreversed[i])
			randomarray[i] = array
		
		
		lineindex = 0
		tempArray = []
		array1Index = 0
		array2Index = 0
		array3Index = 0
		array4Index = 0
		array5Index = 0
		array6Index = 0
		array7Index = 0
		array8Index = 0
		array9Index = 0
		line1ColumnIndex = 0
		line2ColumnIndex = 0
		line3ColumnIndex = 0
		line4ColumnIndex = 0
		line5ColumnIndex = 0
		line6ColumnIndex = 0
		line7ColumnIndex = 0
		line8ColumnIndex = 0
		line9ColumnIndex = 0
		while lineindex < 9:
			columnindex = 0
			dotindex = 0
			innerline = ''
			if lineindex == 0:
				if array1Index >= len(randomarray[lineindex]):
					return []
				innerline = randomarray[lineindex][array1Index]
				array1Index += 1
			elif lineindex == 1:
				if array2Index >= len(randomarray[lineindex]):
					array2Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array2Index]
				array2Index += 1
			elif lineindex == 2:
				if array3Index >= len(randomarray[lineindex]):
					array3Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array3Index]
				array3Index += 1
			elif lineindex == 3:
				if array4Index >= len(randomarray[lineindex]):
					array4Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array4Index]
				array4Index += 1
			elif lineindex == 4:
				if array5Index >= len(randomarray[lineindex]):
					array5Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array5Index]
				array5Index += 1
			elif lineindex == 5:
				if array6Index >= len(randomarray[lineindex]):
					array6Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array6Index]
				array6Index += 1
			elif lineindex == 6:
				if array7Index >= len(randomarray[lineindex]):
					array7Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array7Index]
				array7Index += 1
			elif lineindex == 7:
				if array8Index >= len(randomarray[lineindex]):
					array8Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array8Index]
				array8Index += 1
			else:
				if array9Index >= len(randomarray[lineindex]):
					array9Index = 0
					tempArray.pop()
					lineindex -= 1
					continue
				innerline = randomarray[lineindex][array9Index]
				array9Index += 1
			if self.debugtype:
				print 'current line:',lineindex, ' current line elements:',innerline
			tempArray.append(innerline)
			if self.debugtype:
				print randomarray[lineindex]
				print 'tempArray:'
				print tempArray
			if not self.IsValidSudoku(tempArray):
				tempArray.pop()
				continue
			lineindex += 1
		return tempArray
		
	def MakeArray(self, array):
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
		
		
	def IsValidSudoku(self, results):
		if self.debugtype:
			print 'IsValidSudoku:',results
		linenum = 0
		recArray = ['' for i in range(0,9)]
		while linenum < len(results):
			linesum = ''
			colnum = 0
			while colnum < 9:
				if results[linenum][colnum] != '.':
					ele = results[linenum][colnum]
					if linesum.find(ele) != -1:
						if self.debugtype:
							print 'current line:',linenum,' detail is:',results[linenum]
						return False
					else:
						linesum += ele
					currentloc = linenum/3*3 + colnum/3
					if recArray[currentloc].find(ele) != -1:
						if self.debugtype:
							print 'current loc:',currentloc,' detail is:',recArray[currentloc]
						return False
					else:
						recArray[currentloc] += ele
				colnum += 1
			linenum += 1
			
		colnum = 0
		while colnum < 9:
			linenum = 0
			colsum = ''
			while linenum < len(results):
				if results[linenum][colnum] != '.':
					ele = results[linenum][colnum]
					if colsum.find(ele) != -1:
						if self.debugtype:
							print 'current column:',colnum,' detail is:',colsum,' ele is:',ele
						return False
					else:
						colsum += ele
				linenum += 1
			colnum += 1
		return True
			
		
		
		
if __name__=='__main__':
	cls = ClsSudokuSolver()
	cls.Solver()