

def a(c,p):

	s = p-4
	e = p+5
	if p<5:

		s = 1
		e = c

	if p+5>c:

		s = c-9

		e = c

	if s<=0:

		s = 1

	for i in range(s,e+1):

		print(i)

a(5,3)