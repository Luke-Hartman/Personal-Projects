def solveDP(*values, **kwargs):
	def chooseGen(n, k):
		subset = [i for i in range(k)]
		yield tuple(subset)
		while subset[0] < n - k:
			index = 1
			while subset[-index] == n - index:
				index += 1
			subset[-index] += 1
			for i in range(1, index):
				subset[-index + i] = subset[-index] + i
			yield tuple(subset)
			
	def createComplement(subset, n):
		complement = []
		last = -1
		for i in list(subset) + [n]:
			for j in range(last+1, i):
				complement.append(j)
			last = i
		return tuple(complement)
	
	if 'goal' in kwargs:
		goal = kwargs['goal']
	else:
		goal = 24
	if 'disabledivspeedup' in kwargs and kwargs['disabledivspeedup']:
		def div(a, b):
			if b != 0:
				return a/b
	else:
		def div(a, b):
			if b != 0 and a%b == 0:
				return a//b
	if 'disableaddmulspeedup' in kwargs and kwargs['disableaddmulspeedup']:
		def add(a, b):
			return a + b
		def mul(a, b):
			return a*b
	else:
		def add(a, b):
			if a <= b:
				return a + b
		def mul(a, b):
			if a <= b:
				return a*b
	if 'disablesubspeedup' in kwargs and kwargs['disablesubspeedup']:
		def sub(a, b):
			return a - b
	else:
		def sub(a, b):
			if a <= b:
				return a - b

	ops = [(add, ' + '), (sub, ' - '), (mul, '*'), (div, '/')]
	subproblems = dict()
	
	n = len(values)
	for i in range(n):
		v = values[i]
		key = tuple([i])
		subproblems[key] = [(v, str(v))]
		
	for k in range(2, n + 1):
		for subproblem in chooseGen(n, k):
			possibilities = []
			for i in range(1, k):
				for subset in chooseGen(k, i):
					complement = createComplement(subset, k)
					key1 = tuple(subproblem[j] for j in subset)
					key2 = tuple(subproblem[j] for j in complement)
					subproblem1 = subproblems[key1]
					subproblem2 = subproblems[key2]
					for (v1, s1) in subproblem1:
						for (v2, s2) in subproblem2:
							for (op, symbol) in ops:
								if v1 == v2 and len(key1) < len(key2): continue # Another small speedup
								v = op(v1, v2)
								if v is not None:
									possibilities.append((v, "(%s%s%s)" % (s1, symbol, s2)))
			subproblems[subproblem] = possibilities
	final_results = subproblems[tuple(range(n))]
	solutions = dict()
	for (v, s) in final_results:
		if v == goal and s not in solutions:
			solutions[s] = None
	return list(solutions.keys())
