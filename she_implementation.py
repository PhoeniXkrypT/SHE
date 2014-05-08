import numpy
import math

# defining the big O constant
bigOconstant = 2

def main():
	_lambda = 8
	count = input("Enter number of test cases to be generated : ")
	fails = test(count, _lambda)
	print "Fail count : ", fails
	
	
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

# Function to test for random input values
def test(count, _lambda):
    fails = 0					# to count number of failures in test cases
    rand_range = numpy.random.randint		# to generate random numbers
    for x in range(count):
	sk = secret_key(_lambda)		# function call to generate secret key
	pk = public_key(_lambda, sk)		# function call to generate public key list
	# WARNING works for two bits only
        m1, m2 = rand_range(2), rand_range(2)	# generates two random message bits
	print "M1, M2 : ", m1, ",", m2
        c1, c2 = encrypt(_lambda, pk, m1), encrypt(_lambda, pk, m2)	# calculates two cipher values
	C = genCircuit(rand_range(2), rand_range(2), rand_range(2), rand_range(2))
	dec_msg = decrypt(sk, evaluate(_lambda, C,c1, c2))	# function call to decrypt the cipher from evaluate
	_msg = evaluate(_lambda, C, m1,m2) % 2	# calculates the value when message bits are passed to evaluate i.e. a circuit 
	print "Decrypted values from - cipher, message : ", dec_msg, ",", _msg
        if dec_msg != _msg:
                fails += 1	# increments if the test case fails
    return fails

# Function to generate a large value
# flag = 0 if the generated numbers lower bound is 0 i.e. (0,2**N); else 1
def number_generator(num_of_bits, flag):
	number_count = num_of_bits / 32
	base = 2**32
	rand_num ={}
	if (number_count == 0):
		x = int(numpy.random.uniform(0,2**num_of_bits))
	else :
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
	secret_key = number_generator(eta_value, 1)
	return secret_key
	
# Function to find the different values of public key
def pubkey_distribution(_lambda, secret_key):
	#q_bound = int(math.ceil(math.log((2**gamma(_lambda) / secret_key),2)))
	#q = number_generator(q_bound, 0)
	q = int(numpy.random.uniform(0,2**256))
	r = (1 - 2*(numpy.random.randint(0,2))) * number_generator(_lambda, 0)
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
	r = (1 - 2*(numpy.random.randint(0,2))) * number_generator(rho_dash_value, 0)
	sum_x = 0
	# the summation of xi's for i belongs to S i.e subset of {1,2,3 ... tau}
	for i in random_subset:
		sum_x += public_key[i]
	cipher = (m + 2*r + 2*sum_x ) % pub_key_sorted[0]
	return cipher

# Function to generate a circuit from random values passed to it
def genCircuit(k1, k2, h1, h2):
    def Circuit(c1, c2):
            return c1**k1 + c2**k2 + c1**h1 * c2**h2
    return Circuit

# Function which evaluates the circuit
def evaluate(_lambda, Cir, c1, c2):
	return Cir(c1,c2)

# Function for decryption using the secret key
def decrypt(sec_key, cipher):
	_msg = (cipher % sec_key) % 2
	return _msg

if __name__ == "__main__":
    main()
