from math_tools import hilb_series_to_coefficient_poly as convert
from math import factorial

def parse_macaulay_poly(s):
	#this looks like eg. T3+6T4-3T5
	last_power=-1
	regime = 'coefficient'
	if s[0]=='-':
		coefficient_string='-'
		start_saltus=1
	else:
		coefficient_string=''
		start_saltus=0
	answer=[]
	for c in s[start_saltus:]:
		# print ('c',c,type(c))
		if c=='T':
			regime='exponent'
			exponent_string=''
			if not coefficient_string:
				#monic positive nonconstant leading term
				coefficient=1
			elif coefficient_string[-1] in '+-':
				coefficient_string+='1'
				#monic term
				coefficient=int(coefficient_string)
			else:
				coefficient=int(coefficient_string)
		elif c in ['+','-']:
			if regime=='coefficient':
				#found constant term
				coefficient=int(coefficient_string)
				answer.append(coefficient)
			else:
				if not exponent_string:
					exponent=1
				else:
					exponent=int(exponent_string)
				for _ in range(exponent-len(answer)):
					answer.append(0)
				answer.append(coefficient)
			regime='coefficient'
			coefficient_string=c
		elif regime=='coefficient':
			coefficient_string+=c
		elif regime=='exponent':
			exponent_string+=c
	if regime=='coefficient': #constant poly
		answer.append(int(coefficient_string))
	else:
		if not exponent_string:
			exponent=1
		else:
			exponent=int(exponent_string)
		for _ in range(exponent-len(answer)):
			answer.append(0)
		answer.append(coefficient)
	return(answer)

def process_macaulay_file(mf=macaulay_outfile):
	f= open(mf,'r')
	macaulay_data=f.readlines()
	f.close()
	answer = {}
	for j in range(0,len(macaulay_data),5):
		graph_name=macaulay_data[j].split('Data for graph')[1].strip()
		if graph_name not in answer:
			answer[graph_name]= data_class()
		degree = int(macaulay_data[j+1].split('homological degree')[1].strip())
		denom_power = int(macaulay_data[j+2].split(':')[1].strip())
		num_poly = parse_macaulay_poly(macaulay_data[j+3].split(':')[1].strip())
		valid = len(num_poly) - denom_power - 1
		answer[graph_name].polys[degree]=(num_poly,denom_power,valid)
	for G in answer:
		answer[G].homological_degree=len(answer[G].polys)-1
		length_test=[]
		for i in answer[G].polys:
			length_test.append(int(answer[G].polys[i][2]))
		maxlen = max(length_test)+1
		for i in range(answer[G].homological_degree+1):
			answer[G].Betti_numbers[i]=[]
			for k in range(maxlen+1):
				coef_poly= hilb_series_to_coefficient_poly(answer[G].polys[i][0],answer[G].polys[i][1],k)[::-1]
					#cutting off to get unstable value
				full_coef_poly = hilb_series_to_coefficient_poly(answer[G].polys[i][0],answer[G].polys[i][1])[::-1]
					#not cutting off to get stable prediction
				denom_fact = factorial(answer[G].polys[i][1]-1)
				this_Betti=0
				for j,c in enumerate(coef_poly):
					this_Betti += k**j * c
				if this_Betti % denom_fact:
					print (G, i,k, this_Betti, denom_fact, 'error in fraction',answer[G].polys[i])
					raise(Exception)
				this_Betti =this_Betti // denom_fact
				this_Betti_stable=0
				for j,c in enumerate(full_coef_poly):
					this_Betti_stable += k**j * c
				this_Betti_stable = this_Betti_stable / denom_fact
				##
				answer[G].Betti_numbers[i].append(int(this_Betti))
				if this_Betti != this_Betti_stable:
					answer[G].Betti_number_is_unstable.add((i,k))
		# generate betti numbers
	return answer

def calculate_all_Betti_numbers_and_stable_poly(G):
	G.homological_degree=len(answer[G].poincare_num_poly)-1
	maxlen = max(G.validity.values()) + 1
	for i in range(G.homological_degree+1):
		full_coef_poly = convert(G.poincare_num_poly[i], G.denom_power[i])
			#not cutting off to get stable prediction
		G.stable_poly_normalized[i]=full_coef_poly
		denom_fact = factorial(G.denom_power[i]-1)
		calculate_Betti_numbers_and_stability(G, i, maxlen, denom_fact)

def calculate_Betti_numbers_and_stability(G, i, maxlen, denom_fact):
	G.Betti_numbers[i]=[]
	for k in range(maxlen+1):
		coef_poly= convert(G.poincare_num_poly[i], G.denom_power[i],k)
			#cutting off to get unstable value
		this_Betti=0
		for j,c in enumerate(coef_poly):
			this_Betti += k**j * c
		this_Betti_stable=0
		for j,c in enumerate(G.stable_poly_normalized[i]):
			this_Betti_stable += k**j * c
		if this_Betti != this_Betti_stable:
			G.Betti_number_is_unstable.add((i,k))
		this_Betti, remainder = divmod(this_Betti, denom_fact)
		if remainder:
			raise ParsingError('Error in Fraction with graph {}, i={}, k={}'.format(G.sparse6,i,k))
		G.Betti_numbers[i].append(int(this_Betti))
