import numpy as np
import sys
import copy
import itertools

class Apriori(object):
	def __init__(self):
		self.db = [] # list of transaction item lists
		self.min_support = 1 # default min_support is 1
		self.itemsets = [] # list of tuples, where tuples are (itemset, support), itemset is the set of frequent patterns of size k
		self.k = 0  # index of itemset we are working with now ("actual k" = self.k + 1)
		# self.output_set = []

	# read input from std and store self.db and self.min_support
	def process_input(self):
		message = sys.stdin.readlines()
		# print('db_in: ', db_in)
		
		#first element of message is min_support
		self.min_support = ord(message[0].rstrip()) - 48 # in unicode, 0 is 48
		# print(min_support)

		for i in range(1, len(message)):
			self.db.append(message[i].rstrip().split())
		
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
			# print(self.itemsets)
			
		return self.itemsets


	####################### suppose we have updated k!!!!!!!!
	# generate candidate from F_k-1 to C_k
	# ck is a list of candidate sets
	def candidate(self):
		# print("candidate!")
		ck = []
		# make copy of F_k-1
		itemset = copy.deepcopy(self.itemsets[self.k - 1])
		# print(itemset)
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
					# print('union!')
					# print(c)
					# print('has_infrequent_subset = ', self.has_infrequent_subset(c, self.itemsets[self.k - 1]))
					if not self.has_infrequent_subset(c, self.itemsets[self.k - 1]):
						# print("append")
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

	# print out the result in required format
	def print_output(self):
		for itemlist in self.itemsets:
			if itemlist:
				# print(itemlist)
				for key, value in itemlist:
					s = " ".join(list(key))
					# print(s)
					# print(s[1:])
					# print(value, ' [', s, ']')
					print(str(value) + ' [' + str(s) + ']')
			# output = list(set(itemlist))
			# print(output)




def main():
	a = Apriori()
	a.process_input()
	print(a.apriori())
	a.print_output()

if __name__ == "__main__": 
	main()
