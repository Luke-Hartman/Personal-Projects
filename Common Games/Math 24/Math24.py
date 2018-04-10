import copy

C = copy.deepcopy
Posted = []
def post(string):
	if (string in Posted) is False:
		print(string)
		Posted.append(string)

def Solve(N, Strings):
	t1 = N[0]
	t2 = N[1]
	n1, n2 = t1, t2
	s1, s2 = Strings[0], Strings[1]
	if t2 > t1:
		n1, n2 = t2, t1
		s1, s2 = Strings[1], Strings[0]
	Done = 0
	if len(N) == 2:
		 Done = 1
	#add
	n3 = n1 + n2
	s3 = "({} + {})".format(s1, s2)
	if Done:
		if n3 == 24:
			post(s3)
	else:
		Solve((n3,) + N[2:], [s3] + Strings[2:])
	#subtract
	n3 = n1 - n2
	if n3 > 0:
		s3 = "({} - {})".format(s1, s2)
		if Done:
			if n3 == 24:
				post(s3)
		else:
			Solve((n3,) + N[2:], [s3] + Strings[2:])
	#multiply
	n3 = n1*n2
	s3 = "({}*{})".format(s1, s2)
	if Done:
		if n3 == 24:
			post(s3)
	else:
		Solve((n3,) + N[2:], [s3] + Strings[2:])
	#divide
	n3 = float(n1)/n2
	if True:
		s3 = "({}/{})".format(s1, s2)
		if Done:
			if n3 == 24:
				post(s3)
		else:
			Solve((n3,) + N[2:], [s3] + Strings[2:])

def solve(n1, n2, n3, n4):
	N = [n1, n2, n3, n4]
	Posted = []
	for a in N:
		N2 = C(N)
		N2.remove(a)
		for b in N2:
			N3 = C(N2)
			N3.remove(b)
			c, d = N3[0], N3[1]
			Solve((a, b, c, d), [str(a), str(b), str(c), str(d)])
			Solve((a, b, d, c), [str(a), str(b), str(d), str(c)])

solve(6, 3, 6, 6)
