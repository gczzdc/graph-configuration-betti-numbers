import itertools

def factorial(n):
	if n< 2:
		return 1
	return n * factorial(n-1)

def build_count(x, S):
	ans = 1
	for v in S:
		if len(x[v])<3:
			return 0
		ans *= len(x[v])-2
	return ans

def count_comp(g,S):
	unseen = set(g.edges)
	components = 0
	while unseen:
		components +=1
		used_vertices = set()
		e = unseen.pop()
		if e[0] in S and e[1] in S:
			components += g.edges[e]-1
			continue
		vertices_to_deal_with = set(e)
		while vertices_to_deal_with:
			v = vertices_to_deal_with.pop()
			if v not in S:
				used_vertices.add(v)
				for e2 in list(unseen):
					if v in e2:
						unseen.remove(e2)
						for w in e2:
							if w not in used_vertices:
								vertices_to_deal_with.add(w)
	return components

def count(g,i):
	oneside = (g.stable_poly_normalized[i][-1], g.poincare_denom_power[i]-1)
	best_count = 0
	sum_of_those = 0
	star_iterator = range(len(g.stars))
	for S in itertools.combinations(star_iterator, i):
		components = count_comp(g,S)
		# print (S, components)
		if components > best_count:
			sum_of_those = build_count(g.stars,S)
			best_count = components
		elif components == best_count:
			sum_of_those += build_count(g.stars,S)
	otherside = (sum_of_those, best_count-1)
	# print (oneside, otherside)
	if factorial(oneside[1])*otherside[0] != factorial(otherside[1])*oneside[0]:
		return False
		print ('failure with graph {} and degree {}'.format(g.sparse6, i))
	return True

def test(gg):
	ans = set()
	for g in gg:
		for i in range(2, len(g.stable_poly_normalized)):
			if not count(g,i):
				ans.add(g)
	return ans