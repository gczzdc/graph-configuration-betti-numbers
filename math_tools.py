import numpy as np

def hilb_series_to_coefficient_poly(numerator, denom_power, cutoff=-1):
	# print (numerator, type(numerator))
	#hilb series is of the form numerator/(1-T)^denom_power
	#numerator is formatted as an array starting with LOWEST power.
	#start by generating the formula for coefficients
	#output formatted starting with LOWEST power
	#should be divided by (denom_power-1) factorial
	ans = []
	if denom_power==0:
		raise ValueError('Conversion not implemented in this function when rational function is a polynomial')
	for i in range(len(numerator[:min(cutoff,len(numerator)-1)])+1):
		this_term=[numerator[i],]
		for j in range(1,denom_power):
			this_term=np.polymul(this_term, [1,j-i])
		ans=np.polyadd(ans,this_term)
	return [int(n) for n in ans][::-1]