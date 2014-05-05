import numpy

bigOconstant = 2
lambda_value = 8

def main():
	sk = secret_key(lambda_value)
	print "Secret Key\n", int(sk)
	pk = public_key(sk)
	print "Public Key Values\n", pk
	random_subset = generate_random_subset(tau(lambda_value))
	m = numpy.random.randint(0,2)
	print " m = ", m
	c = encrypt(pk, m, random_subset)
	print "c = ", c

def eta(lambda_value):
	return (bigOconstant * lambda_value * lambda_value)
def gamma(lambda_value):
	return (bigOconstant * lambda_value**5)
def tau(lambda_value):
	return (gamma(lambda_value) + lambda_value)
def rho_dash(lambda_value):
	return (2*lambda_value)

def secret_key(lambda_value):
	eta_value = eta(lambda_value)
	number_count = eta_value / 32
	base = 2**32
	while True :
		rand_numbers = [int(numpy.random.uniform(0,2**32)) for x in xrange(number_count -1)]
		if (int(rand_numbers[0]) & 1) :
			break
	concatenated_number = rand_numbers[0] + rand_numbers[1] * base + rand_numbers[2] * base**2
	msb_number = int(numpy.random.uniform(2**31,2**32))
	secret_key = concatenated_number + (msb_number * base**3)
	return secret_key

def distribution(secret_key):
	#q_bound = 2**gamma(lambda_value) / secret_key
	q = int(numpy.random.uniform(0,2**256))
	r = int(numpy.random.uniform(-2**lambda_value,2**lambda_value))
	x = secret_key * q + r
	return x

def public_key(secret_key):
	while True:
		pubkey = [distribution(secret_key) for i in range(tau(lambda_value))]
		pubkey_max = max(pubkey)	
		pubkey_mod_sk = pubkey_max % secret_key
		if (pubkey_max & 1) and (pubkey_mod_sk % 2 ==0):
			break
	return pubkey

def generate_random_subset(_tau):
	set_size = numpy.random.randint(1, _tau)
	S = set()
	while len(S) < set_size:
		x = numpy.random.randint(1, _tau)
		S.add(x)
	return S
	
def encrypt(public_key, m, S):
	# c = (m+2r+2 xi's) mod x0
	pub_key_sorted = sorted(public_key, reverse=True)
	rho_dash_value = rho_dash(lambda_value)
	r = int(numpy.random.randint(-2**rho_dash_value, 2**rho_dash_value))
	sum_x = 0
	for i in S:
		sum_x += public_key[i]	
	cipher = (m + 2*r + 2*sum_x ) % pub_key_sorted[0]
	return cipher

if __name__ == "__main__":
    main()
