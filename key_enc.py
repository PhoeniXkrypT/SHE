import numpy

# defining the big O constant and lambda value
bigOconstant = 2

def main():
	_lambda = 8
	sk = secret_key(_lambda)	# function call to generate secret key
	#print "Secret Key\n", int(sk)
	pk = public_key(_lambda, sk)		# function call to generate public key list
	#print "Public Key Values\n", pk
	cipher = {}
	for i in range(3):
		m = numpy.random.randint(0,2)
		print " Message = ", m
		c = encrypt(_lambda, pk, m)
		print "Cipher = ", c
		cipher[i] = c
	print "C = ", cipher
	_eval = evaluate(_lambda, cipher)
	print "Eval = ", _eval
	dec = decrypt(sk, _eval)
	print dec

# Function to calculate eta value from the security parameter lambda
def eta(_lambda):			# eta is bit length of secret key 
	return (bigOconstant * _lambda * _lambda)
# Function to calculate gamma value from the security parameter lambda
def gamma(_lambda):
	return (bigOconstant * _lambda**5)
# Function to calculate tau value from the security parameter lambda
def tau(_lambda):			# tau is number of integers in public key
	return (gamma(_lambda) + _lambda)
# Function to calculate rho' value from security parameter lambda
def rho_dash(_lambda):
	return (2*_lambda)

# Function to generate a large value
# flag = 0 if the generated numbers lower bound is 0 i.e. (0.2**N); else 1
def number_generator(num_of_bits, flag):
	number_count = num_of_bits / 32
	base = 2**32
	rand_num ={}
	for i in range(number_count):
		rand_num[i] = int(numpy.random.uniform(0,2**32))
	rand_num[0] = ((rand_num[0] & ~1 ) + 1)
	if (flag == 1) :
		rand_num[number_count-1] = ((rand_num[number_count-1] & ~2**31 ) + 2**31)
	x=0
	# number = x0*base**0 + x1*base**1 + x2*base**2 + x3*base**3 + ...
	for i in range(number_count):
		x +=  rand_num[i] * base**i
	return x

# Function to calculate the secret key which is an odd eta-bit integer
def secret_key(_lambda):
	eta_value = eta(_lambda)
	print "eta = ", eta_value
	secret_key = number_generator(eta_value, 1)
	return secret_key
	
# Function to find the different values of public key
def pubkey_distribution(_lambda, secret_key):
	#q_bound = 2**gamma(_lambda) / secret_key
	q = int(numpy.random.uniform(0,2**256))		
	r = (1 - 2*(numpy.random.randint(0,2))) * number_generator(2**_lambda, 0)
	x = secret_key * q + r
	return x
	
# Function to calculate the public key list
def public_key(_lambda, secret_key):
	while True:
		pubkey = [pubkey_distribution(_lambda, secret_key) for i in range(tau(_lambda))]
		pubkey_max = max(pubkey)	# get largest value from list	
		pubkey_mod_sk = pubkey_max % secret_key
		# loop till largest value is odd and the value modulus secret key is even
		if (pubkey_max & 1) and (pubkey_mod_sk % 2 == 0):
			break
	return pubkey

# Function to generate a random subset S from {1, 2, 3, .... tau}
def generate_random_subset(_tau):
	set_size = numpy.random.randint(1, _tau)
	S = set()
	while len(S) < set_size:
		x = numpy.random.randint(1, _tau)
		S.add(x)
	return S

# Function to encrypt a bit m from {0,1}	
def encrypt(_lambda, public_key, m):
	random_subset = generate_random_subset(tau(_lambda))
	# c = (m+2r+2*xi's) mod x0
	# Sorting in descending order
	pub_key_sorted = sorted(public_key, reverse=True)
	rho_dash_value = rho_dash(_lambda)
	r = (1 - 2*(numpy.random.randint(0,2))) * number_generator(2**rho_dash_value, 0)
	sum_x = 0
	# the summation of xi's for i belongs to S i.e subset of {1,2,3 ... tau}
	for i in random_subset:
		sum_x += public_key[i]
	cipher = (m + 2*r + 2*sum_x ) % pub_key_sorted[0]
	return cipher

def evaluate(_lambda, ciphers):
	C = ciphers[0]+ciphers[1]*ciphers[2]
	print "C = ", C
	return C

def decrypt(sec_key, cipher):
	eval_msg = (cipher % sec_key) % 2
	return eval_msg

if __name__ == "__main__":
    main()
