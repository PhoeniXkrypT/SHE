import numpy

bigOconstant = 2
lambda_value = 8

def main():
	sk = secret_key(lambda_value) # function call to generate secret key
	print "Secret Key\n", int(sk)
	pk = public_key(sk) # function call to generate public key list
	print "Public Key Values\n", pk

# Function to calculate eta value from the security parameter lambda
def eta(lambda_value):
	return (bigOconstant * lambda_value * lambda_value)
# Function to calculate gamma value from the security parameter lambda
def gamma(lambda_value):
	return (bigOconstant * lambda_value**5)
# Function to calculate tau value from the security parameter lambda
def tau(lambda_value):
	return (gamma(lambda_value) + lambda_value)

# Function to calculate the secret key which is an odd integer
def secret_key(lambda_value):
	eta_value = eta(lambda_value)
	number_count = eta_value / 32
	base = 2**32
	while True :
		rand_numbers = [int(numpy.random.uniform(0,2**32)) for x in xrange(number_count -1)]
		if (int(rand_numbers[0]) & 1) :
			break
	#print "Rand nums ", rand_numbers
	concatenated_number = rand_numbers[0] + rand_numbers[1] * base + rand_numbers[2] * base**2
	msb_number = int(numpy.random.uniform(2**31,2**32))
	#print "MSB ", msb_number
	secret_key = concatenated_number + (msb_number * base**3)
	return secret_key

def distribution(secret_key):
	#q_bound = 2**gamma(lambda_value) / secret_key
	q = int(numpy.random.uniform(0,2**256))
	r = int(numpy.random.uniform(-2**lambda_value,2**lambda_value))
	x = secret_key * q + r
	return x
# Function to calculate the public key
def public_key(secret_key):
	while True:
		pubkey = [distribution(secret_key) for i in range(tau(lambda_value))]
		pubkey_max = max(pubkey)	
		pubkey_mod_sk = pubkey_max % secret_key
		if (pubkey_max & 1) and (pubkey_mod_sk % 2 == 0):
			break
	return pubkey

if __name__ == "__main__":
    main()
