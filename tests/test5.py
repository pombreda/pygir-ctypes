def _merge_mro(seqs):
	res = []
	i = 0
	
	while 1:
		nonemptyseqs = [seq for seq in seqs if seq]
		
		if not nonemptyseqs:
			return res
		
		i += 1
		
		for seq in nonemptyseqs:
			cand = seq[0]
			nothead = [s for s in nonemptyseqs if cand in s[1:]]
			
			if nothead:
				cand = None
			else:
				break
		
		if not cand:
			raise GIError("Inconsistent hierarchy")
		
		res.append(cand)
		
		for seq in nonemptyseqs:
			if seq[0] == cand:
				del seq[0]

def _calc_mro(C):
	return _merge_mro([[C]] + map(_calc_mro, C.__bases__) + [list(C.__bases__)])

def _mro(bases):
	segs = []
	
	for base in bases:
		segs.append(_calc_mro(base))
	
	return _merge_mro(segs)

if __name__ == '__main__':
	class F(object): pass
	class E(object): pass
	class D(object): pass
	class C(D, F): pass
	class B(D, E): pass
	class A(B, C): pass
	
	print(_mro([A, D, E, F]))
