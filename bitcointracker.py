import os, sys
import urllib.request
import json
import time
import math

def request(full_api_url):
	res = ""
	try:
		url = urllib.request.urlopen(full_api_url)
		output = url.read().decode('utf-8')
		res = json.loads(output)
		url.close()
	except:
		res = ""
	return res

VSIZE = 11
HSIZE = 40
PRICE_RANGE = 500
price = []
for i in range(0,HSIZE):
	price.append(-1)

def main():

	loop = 1

	while loop:
		os.system('cls' if os.name == 'nt' else 'clear')
		
		''' Update '''
		coin = "" if (len(sys.argv) == 1) else sys.argv[1]
		res = request("https://api.coinmarketcap.com/v1/ticker/"+coin)
		if res == "":
			continue
			
		PRICE_RANGE = 2 * (10 * math.log(float(res[0]["price_usd"])))
		
		''' Load array '''
		for i in range(0,HSIZE-1):
			price[i] = price[i+1]
		price[int(HSIZE*(3/4))] = float(res[0]["price_usd"])
		
		''' Get frame information '''
		min_price = int(min(list(filter((-1).__ne__, price))) - (PRICE_RANGE/2))
		
		''' Print output -- Also a file output '''
		f = open(res[0]["name"].lower()+".chart","w")
		
		s = "" + res[0]["name"] + " at " + res[0]["price_usd"] + " USD";
		print(s)
		f.write(s+"\n")
		
		for i in range(0,VSIZE):
			curprice = min_price + PRICE_RANGE * ((VSIZE-i)/VSIZE)
			lowerprice = curprice - PRICE_RANGE/10
			if max(price) < 30:
				num = int(curprice)
			else:
				num = int(curprice)
			if i != 0 and i != VSIZE - 1 and i != int(VSIZE/2):
				string = "      |"
			else:
				string = '{0:<5}'.format(str(num)) + " |"
			for j in range(0,HSIZE):
				if (price[j] <= curprice and price[j] >= lowerprice):
					string = string + "+"
				else:
					string = string + " "
			print(string)
			f.write(string + "\n")
		
		print()
		
		f.close()
		
		''' Sleep til the next cycle '''
		time.sleep(60*10)
		
	return 0
	
main()
