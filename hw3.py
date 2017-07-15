# import numpy as np
import sys
import copy
import itertools

class Apriori(object):
	def __init__(self):
		self.db = [] # list of transaction item lists
		self.min_support = 1 # default min_support is 1
		self.itemsets = [] # list of tuples, where tuples are (itemset, support), itemset is the set of frequent patterns of size k
		self.k = 0  # index of itemset we are working with now ("actual k" = self.k + 1)
		self.closet = [] # list of close sets, structure same as self.itemsets
		self.maxset = [] # list of max sets, structure same as self.itemsets
		# self.output_set = []

	# read input from std and store self.db and self.min_support
	def process_input(self):
		# a more elegant way of reading input:
		self.min_support = int(input())
		inp = "hello"
		while inp != "":
			inp = input()
			self.db.append(inp.rstrip().split())


		# message = sys.stdin.readlines()
		# # print('db_in: ', db_in)
		
		# #first element of message is min_support
		# self.min_support = ord(message[0].rstrip()) - 48 # in unicode, 0 is 48
		# # print(min_support)

		# for i in range(1, len(message)):
		# 	self.db.append(message[i].rstrip().split())
		
		# print("database: ", self.db)

	# generate 1-itemset
	def one_itemset(self):
		# temporary container for 1-itemset 
		itemset = []
		# for each transaction
		for i in range(len(self.db)):
			# for each item in one transaction
			for j in range(len(self.db[i])):
				# print("examine elemnent ", self.db[i][j])
				# find the current set of one-items in itemset
				keys = [k for (k, v) in itemset] 
				# print("Keys: ", keys)
				# itemset1 = [(k, v + 1) if (k == set(self.db[i][j])) else (k, v) for (k, v) in itemset]
				# make the 1-item an itemset with 1 element
				s = set()
				s.add(self.db[i][j])
				# if itemset already has this item, update the itemset
				if s in keys:
					# print(self.db[i][j], "is in keys")
					itemset = [(k, v + 1) if (k == s) else (k, v) for (k, v) in itemset]
				# if itemset does not have this item yet, add a tuple (1-itemset, 1) to itemset
				else:
					# print(self.db[i][j], "is not in keys")
					itemset.append((s, 1))
				# print("itemset: ", itemset)
					# itemset = copy.deepcopy(itemset1)
				# 	itemset[set(self.db[i][j])] += 1
				# else:
				# 	itemset[set(self.db[i][j])] = 1
		self.itemsets.append(itemset)
		self.prune()
		# print("one itemset: ", self.itemsets)
		# self.k += 1

	def apriori(self):
		# find frequent 1 itemsets
		self.one_itemset()
		# print(self.k - 2)
		# print(len(self.itemsets[self.k - 2]))
		while self.itemsets[self.k]:
			# print('k = ', self.k)
			# print('F_k-1 = ', self.itemsets[self.k])
			# increment k to next level
			self.k += 1		
			ck = self.candidate()
			# print('C_k = ', ck)
			# for all itemsets in C_k
			fk = [] # store tuples in F_k
			for c in ck:
				count = 0
				# count how many times the candidate set appears in db
				for i in self.db:
					if c.issubset(set(i)):
						count += 1
				if (count >= self.min_support) and ((c, count) not in fk):
					fk.append((c, count))
			# print('F_k = ', fk)
			# append F_k to list of itemsets
			self.itemsets.append(fk)	
		# for i in self.itemsets:
		# 	print(i)
			
		# return self.itemsets


	####################### suppose we have updated k!!!!!!!!
	# generate candidate from F_k-1 to C_k
	# ck is a list of candidate sets
	def candidate(self):
		# print("candidate!")
		ck = []
		# make copy of F_k-1
		itemset = copy.deepcopy(self.itemsets[self.k - 1])
		# print("itemset on level", self.k - 1, " is:", itemset)
		# print("k = ", self.k)
		for k1, v1 in self.itemsets[self.k - 1]:
			for k2, v2 in itemset:
				# print("k1 = ", k1, "k2 = ", k2)
				# convert sets k1, k2 to lists
				l1 = list(k1)
				l2 = list(k2)
				ll1 = l1[:(len(l1) - 2)] # ll1: l1 without last element
				ll2 = l2[:(len(l2) - 2)] # ll2: l2 without last element
				
				# if two sets are equal except last item, union/join them
				if ll1 == ll2 and l1[-1] != l2[-1]:
					c = k1.union(k2)
					# print('union result:', c, "len(c) = ", len(c))
				
					# print('has_infrequent_subset = ', self.has_infrequent_subset(c, self.itemsets[self.k - 1]))
					if not self.has_infrequent_subset(c, self.itemsets[self.k - 1]) and len(c) == self.k + 1:
						# print("append ", c)
						ck.append(c)
		# self.level += 1
		return ck

	# check whether c has infrequent subsets in itemset
	# c: candidate k-itemset; itemset: frequent (k-1)-itemsets
	def has_infrequent_subset(self, c, itemset):
		# print("has_infrequent_subset!")
		# subsets is a list of subset tuples of F_k-1
		L = [k for (k, v) in itemset]
		# print("L = ", L)
		# print("k = ", self.k)
		subsets = list(itertools.combinations(c, self.k))
		# print('subsets of c: ', subsets)
		for i in subsets:
			if set(i) not in L:
				return True
		return False

	# prune current level k: from C_k to F_k
	def prune(self):
		self.itemsets[self.k] = [(k, v) for (k, v) in self.itemsets[self.k] if v >= self.min_support]
		# for key, value in self.itemsets[self.k - 1]:
		# 	print(key, ', ', value)
		# 	if  value < self.min_support:
		# 		print("delete ", key)
		# 		self.itemsets[self.k - 1].remove((key, value))
		self.itemsets[self.k].sort()
		# print(self.itemsets[self.k - 1])

	# algorithm to mine the clsoed frequent patterns from the db
	def mine_closet(self):
		# for frequent itemsets of all sizes
		for i in range(0, len(self.itemsets) - 1): # should not reach the empty set in self.itemsets
			close = []
			# j = (set(pattern), count)
			# for all frequent items of size i
			for kj, vj in self.itemsets[i]:
				# print("")
				# print("kj = ", kj, "vj = ", vj)
				# is_close = True
				# for kk, vk in self.itemsets[i+1]:
				# 	print("kk = ", kk, "vk = ", vk)
				# 	if (kj.issubset(kk)) and (vj <= vk):
				# 		is_close = False
				# if for all frequent itemsets one size bigger, they are either not subset of kj 
				# or count(aka, vj) is larger than the bigger frequent itemset, it is closed
				if all(((not kj.issubset(kk)) or (vj > vk)) for kk, vk in self.itemsets[i+1]):
				# if is_close: 
				# 	print("is_close = True")
					close.append((kj, vj)) 
				# for kk, vk in range(len(self.itemsets[i+1])):
				# 	if (kj not in kk) or (vj > vk):
			# print(close)
			self.closet.append(close)

	# algorithm to mine the clsoed frequent patterns from the db
	def mine_maxset(self):
		for i in range(0, len(self.itemsets) - 1): # should not reach the empty set in self.itemsets
			max_temp = []
			# for all frequent items of size i
			for kj, vj in self.itemsets[i]:
				# if for all frequent itemsets one size bigger, they are either not subset of kj 
				# it is a max pattern
				if all((not kj.issubset(kk)) for kk, vk in self.itemsets[i+1]):
					max_temp.append((kj, vj)) 
				
			# print(close)
			self.maxset.append(max_temp)



	# print out the result (apriori: 1; closed set: 2; max set: 3) in required format
	def print_output(self, list_to_print):
		if list_to_print == 1: 
			flat_list = []
			# flatten all frequent patterns (self.itemsets)
			for itemlist in self.itemsets:
				if itemlist:
					for key, val in itemlist:
						l = list(key)
						l.sort()
						flat_list.append((l, val))
			# print(flat_list)
			# sort the falttened list (set(pattern), count)
			flat_list = [(list(key), val) for key, val in flat_list] # covert set(pattern) to list
			flat_list.sort(key = lambda x: x[0]) # sort by pattern
			flat_list.sort(key = lambda x: x[1], reverse = True) #sort by count in descending order
			for key, value in flat_list:
				# key.sort()
				# print('l = ', l)
				s = " ".join(key)
				# print(s)
				# print(s[1:])
				# print(value, ' [', s, ']')
				print(str(value) + ' [' + str(s) + ']')
				
		elif list_to_print == 2:
			flat_list = []
			# flatten all frequent patterns (self.itemsets)
			for itemlist in self.closet:
				if itemlist:
					for key, val in itemlist:
						l = list(key)
						l.sort()
						flat_list.append((l, val))
			# print(flat_list)
			# sort the falttened list
			flat_list = [(list(key), val) for key, val in flat_list]
			flat_list.sort(key = lambda x: x[0])
			flat_list.sort(key = lambda x: x[1], reverse = True)
			for key, value in flat_list:
				# key.sort()
				# print('l = ', l)
				s = " ".join(key)
				# print(s)
				# print(s[1:])
				# print(value, ' [', s, ']')
				print(str(value) + ' [' + str(s) + ']')

		elif list_to_print == 3:
			flat_list = []
			# flatten all frequent patterns (self.itemsets)
			for itemlist in self.maxset:
				if itemlist:
					for key, val in itemlist:
						l = list(key)
						l.sort()
						flat_list.append((l, val))
			# print(flat_list)
			# sort the falttened list
			flat_list = [(list(key), val) for key, val in flat_list]
			flat_list.sort(key = lambda x: x[0])
			flat_list.sort(key = lambda x: x[1], reverse = True)
			for key, value in flat_list:
				# key.sort()
				# print('l = ', l)
				s = " ".join(key)
				# print(s)
				# print(s[1:])
				# print(value, ' [', s, ']')
				print(str(value) + ' [' + str(s) + ']')
			
		else:
			return
			



def main():
	# apriori 
	a = Apriori()
	a.process_input()
	a.apriori()
	a.print_output(1)
	# closed sets
	a.mine_closet()
	print("")
	a.print_output(2)
	# max sets
	print("")
	a.mine_maxset()
	a.print_output(3)


if __name__ == "__main__": 
	main()
