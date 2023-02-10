import time
import datetime

# Global Constant Variable to store the service options for products.
PRODUCTS = {
	"Ladies": {
		"Dress": {"type": "Ladies", "standard": 8.00, "specialist": 11.20},
		"Eve Dress": {"type": "Ladies", "standard": 0.00, "specialist": 21.00},
		"2 Pc Suit": {"type": "Ladies", "standard": 12.00,"specialist": 16.80},
		"Jacket": {"type": "Ladies", "standard": 7.50, "specialist": 9.10},
		"Shirt": {"type": "Ladies", "standard": 6.50, "specialist": 9.10},
		"Blouse": {"type": "Ladies", "standard": 6.50, "specialist": 9.10},
	},
	"Gentlemen": {
		"2 Pc Suit": {"type": "Gentlemen", "standard": 12.00, "specialist": 16.80},
		"2 Pc Eve Suit": {"type": "Gentlemen", "standard": 0.00, "specialist": 16.80},
		"Jacket": {"type": "Gentlemen", "standard": 7.50, "specialist": 10.50},
		"Trousers": {"type": "Gentlemen", "standard": 6.50, "specialist": 9.10},
		"Shirt": {"type": "Gentlemen", "standard": 6.50, "specialist": 9.10},
		"Coat": {"type": "Gentlemen", "standard": 9.95, "specialist": 13.93}
	}
}

def createReceiptItemRow(length, items):
	"""
	The main function used to create a receipt. It will loop over every item, creating a row displaying the data with the correct amount
	of padding.

	Parameters:
	length		: int	The longest item name that exists out of all products.
	items		: List	The list of all items that they have had a placed a service on.

	Returns:
	output		: str	All the item rows in a string, seperated by a new line
	longest		: int	The length of the longest item row
	"""
	# Constants
	NAME_LENGTH = length
	TYPE_LENGTH = 3
	SERVICE_LENGTH = 3
	PRICE_LENGTH = 5

	output = ""
	longest = 0
	for item in items: # loop over every item in the list items.
		row = f"|  " # start the row
		row += f"{item[0]:<{NAME_LENGTH}}   " # concatenate the item name, and align text left with a max width of NAME_LENGTH
		row += f"{item[1]:<{TYPE_LENGTH}}   " # concatenate the clothing type, and align text left with a max width TYPE_LENGTH
		row += f"{item[2]:<{SERVICE_LENGTH}}     " # concatenate the service type, and align text left with a max width SERVICE_LENGTH
		row += f"£{item[3]:>{PRICE_LENGTH}.2f}" # concatenate the price, align text left with a max width PRICE_LENGTH and restrict to 2 dec places
		row += f"  |" # end row
		if len(row) > longest: # if this row is longest so far...
			longest = len(row) # update longest variable
		output += row + "\n" # add to the overall output, and add new line.
	
	return output, longest

def createReceiptTitle(maxLength):
	"""
	Function that will create the title row of the receipt.

	Parameters:
	maxLength	: int	Positive integer which is the length of the longest item row

	Returns:
	output		: str	The string which contains the title, surrounded by padding.
	"""
	TITLE_TEXT = "Receipt" # Constant
	length = maxLength - len(TITLE_TEXT) - 2 # Take length of title away from maxLength finding remanining space. Subtract 2 because of the start&end "|"

	if (length % 2) != 0: # if the length divided by 2 has a remainder (odd number)
		length = length // 2 # whole integer division
		output = f"|{' '*length}{TITLE_TEXT}{' '*length} |\n" # equal spacing on each side, the title in the middle. An extra space at the end as it is odd.
	else:
		length = length // 2 # whole integer division
		output = f"|{' '*length}{TITLE_TEXT}{' '*length}|\n" # equal spacing on each side, the title in the middle.
	
	return output

def createReceiptBar(maxLength):
	"""
	This function simply creates a row which will be used to seperate different sections.

	Parameters:
	maxLength	: int	Positive integer which is the length of the longest item row

	Returns:
	output		: str	A string of the seperating bar, ending with a new line.
	"""
	length = maxLength - 2 # Subtract 2 because the start and end "+"
	output = f"+{'-'*length}+\n" # start with "+" and then length number of "-" finally ending with a "+"
	return output

def createReceiptBlank(maxLength):
	"""
	Function which will create a "blank" (only containing the start and end "|") row. Used to create spacing.

	Parameters:
	maxLength	: int	Positive integer which is the length of the longest item row

	Returns:
	output		: str	A string consisting of padding (" ") and the start and end "|"
	"""
	length = maxLength - 2 # Subtract 2 because of the start and end "|"

	if (maxLength % 2) != 0: # if the maxLength divided by 2 has a remainder (odd number)
		output = f"|{' '*length} |\n" # start with "|" and then length number of spaces, ending with a "|". This has an extra space first because odd.
	else:
		output = f"|{' '*length}|\n" # start with "|" and then length number of spaces, ending with a "|". 

	return output

def createReceiptOrderRow(maxLength, items):
	"""
	Function which creates a row displaying the order number and centers it using maxLength to equally pad each side.

	Parameters:
	maxLength	: int	Positive integer which is the length of the longest item row
	items		: List	A 2d list of items - each item containing a name, clothing type, service type, order number, and price.

	Returns:
	output		: str	A string containing the row, ending with a new line.
	"""
	orderNumber = "Order: " + items[0][4] # Get the order number
	orderNumberLength = len(orderNumber) # Get the order strings length
	length = maxLength - orderNumberLength - 2 # Get the remaining space, subtracting the start&end "|" and order string length

	if (length % 2) != 0: # if the length divided by 2 has a remainder (is odd)
		length = length // 2 # whole integer division
		output = f"|{' '*length}{orderNumber}{' '*length} |\n" # start "|" - equally padding with orderNumber in middle - end "|". Extra space because odd.
	else:
		length = length // 2 # whole integer division
		output = f"|{' '*length}{orderNumber}{' '*length}|\n" # start "|" - equally padding with orderNumber in middle - end "|".

	return output

def createReceiptTotalsRow(maxLength, items):
	"""
	Function creating the rows for totals (subtotal, savings, total, and total inc. VAT).

	Parameters:
	maxLength	: int	Positive integer which is the length of the longest item row
	items		: List	A 2d list of items - each item containing a name, clothing type, service type, order number, and price.

	Returns:
	output		: str	A string containing the row, ending with a new line.
	"""
	MAX_LENGTH = 14 # Constant defining the max heading length ("Total inc. VAT")
	PADDING = (maxLength - 4) - (MAX_LENGTH + 9) # Calculate fill padding, add 9 because of 3 gap and 6 price length ("   £24.52")
	
	# Constant headings, needed to format string
	SUBTOTAL = "Subtotal"
	SAVINGS = "Savings"
	TOTAL = "Total"
	TOTALVAT = "Total inc. VAT"

	totals = calculateTotals(items) # Get all the totals, returned in a dictionary

	# Fill the left padding with spaces, heading left alligned, totals right alligned and 2 decimal places.
	output = f"|{' '*PADDING}{SUBTOTAL:<{MAX_LENGTH}}   £{totals['subtotal']:>5.2f}  |\n"
	output += f"|{' '*PADDING}{SAVINGS:<{MAX_LENGTH}}   £{totals['savings']:>5.2f}  |\n"
	output += f"|{' '*PADDING}{TOTAL:<{MAX_LENGTH}}   £{totals['total']:>5.2f}  |\n"
	output += f"|{' '*PADDING}{TOTALVAT:<{MAX_LENGTH}}   £{totals['totalVAT']:>5.2f}  |\n"

	return output

def createReceipt(length, items):
	"""
	Function used to create the receipt for a order containing a number of items.

	Parameters:
	length	: int	A positive integer, representing the longest item name.
	items	: list	A 2d list of items - each item containing a name, clothing type, service type, order number, and price.

	Returns:
	output	: str	The full string containing the receipt ready to be outputted to a file.
	"""

	# Create the different components used to make the receipt.
	itemRows, itemRowsLength = createReceiptItemRow(length, items)
	bar = createReceiptBar(itemRowsLength)
	title = createReceiptTitle(itemRowsLength)
	order = createReceiptOrderRow(itemRowsLength, items)
	blank = createReceiptBlank(itemRowsLength)
	totals = createReceiptTotalsRow(itemRowsLength, items)

	receipt = bar + title + bar + order + blank + itemRows + blank + totals + bar # This concatenates all the components to get the final receipt.

	return receipt

def createTagBar(length):
	"""
	A function used to create the bar used to seperate different clothing orders.

	Parameters:
	length		: int	This is the longest item names length

	Returns:
	output		: str	A string containing the bar
	"""
	# Constants (all have add 4, because the 2 padding on left and right)
	NAME_LENGTH = length + 4
	TYPE_LENGTH = 3 + 4
	SERVICE_LENGTH = 3 + 4
	ORDER_LENGTH = 11 + 4

	# + is used for when a column ends / the start and end
	output = f"+{'-'*NAME_LENGTH}"
	output += f"+{'-'*TYPE_LENGTH}"
	output += f"+{'-'*SERVICE_LENGTH}"
	output += f"+{'-'*ORDER_LENGTH}+\n"

	return output

def createTagItemRow(length, items, bar):
	"""
	A function that will go through every clothing items order and create its row.

	Parameters:
	length		: int	The longest item name that exists. 
	items		: List	A list of all clothing items they have got a service for.
	bar			: str	This is the created bar used to seperate items.

	Returns:
	output		: str	This is a string containing all the item rows, ready to be combined and make all tags for the order.
	"""
	# Constants
	NAME_LENGTH = length # longest item name
	TYPE_LENGTH = 3
	SERVICE_LENGTH = 3
	ORDER_LENGTH = 11

	output = ""
	for item in items: # loop over every item they have got a service for
		row = f"|  "
		row += f"{item[0]:<{NAME_LENGTH}}  |" # concatenate the item name, and align text left with a max width of NAME_LENGTH
		row += f"  {item[1]:<{TYPE_LENGTH}}  |" # concatenate the clothing type, and align left with a max width of TYPE_LENGTH
		row += f"  {item[2]:<{SERVICE_LENGTH}}  |" # concatenate the service type, and align left with a max width of SERVICE_LENGTH
		row += f"  {item[4]:<{ORDER_LENGTH}}  |\n" # concatenate the order number, and align left with a max width of ORDER_LENGTH. End with a new line.
		output += row # concatenate the created row to the output
		output += bar # add a seperating bar

	return output

def createTag(length, items):
	"""
	This function is used to create the tag for a given order.

	Parameters:
	length		: int	This is the longest item names length
	items		: List	The list of items they have got a service on.

	Returns:
	tag			: str	The full string of tags to be stored in a file and printed.
	"""
	bar = createTagBar(length)
	orderRows = createTagItemRow(length, items, bar)

	tag = bar + orderRows

	return tag

def getLongestItemName(items):
	"""
	This function is used to get the longest item name in a given array.

	Parameters:
	items		: List	The list of items they have got a service on.

	Returns:
	longest		: int	Length of longest item name
	"""
	longest = 0
	for item in items: # loop over every item
		if len(item) > longest: # if the current item is longer
			longest = len(item) # set new longest

	return longest

def calculateSubtotal(items):
	"""
	This function is used to calculate the subtotal of given items.

	Parameters:
	items		: List	The list of items they have got a service on.

	Returns:
	subtotal	: float	Subtotal of all items.
	"""
	subtotal = 0
	for item in items: # loop over every item
		subtotal += item[3] # add to subtotal
	return subtotal

def calculateDiscount(subtotal):
	"""
	This function is used to calculate any discount they get on the order.

	Parameters:
	subtotal	: float	The subtotal of all items in the order.

	Returns:
	discounts	: dict	A dictionary of the new subtotal, and the savings made.
	"""
	if subtotal > 30.00: # if there order is greater than £30
		newSubtotal = subtotal * 0.85 # save 15%
		savings = subtotal - newSubtotal
	elif subtotal > 15.00: # if not, is it greater than £15
		newSubtotal = subtotal * 0.90 # save 10%
		savings = subtotal - newSubtotal
	else: # no savings
		newSubtotal = subtotal
		savings = 0
	
	discounts = {"subtotal": newSubtotal, "savings": savings}
	return discounts

def calculateVAT(subtotal):
	"""
	This function calculates the final total from a given subtotal.

	Parameters:
	subtotal	: float	The subtotal of an order, after any savings.

	Returns:
	totalIncVat	: float	The final total including VAT.
	"""
	VAT = 1.20
	totalIncVAT = subtotal * VAT
	return totalIncVAT
	
def calculateTotals(items):
	"""
	This function calculates all total data, and returns to be used in the receipt.

	Parameters:
	items		: List	The list of items they have got a service on.

	Returns:
	totals		: dict	Dictionary containing the subtotal, savings, total and total inc. VAT.
	"""
	subtotal = calculateSubtotal(items)
	savings = calculateDiscount(subtotal)
	total = calculateVAT(savings["subtotal"])

	totals = {"subtotal": subtotal, "savings": savings["savings"], "total": savings["subtotal"], "totalVAT": total}
	return totals

def saveToFile(filename, content):
	"""
	This function is used to save data to a file.

	Parameters:
	filename	: str	The filename string, including file extention.
	content		: str	The string containing all data to be saved to the file.
	"""
	try:
		with open(filename, "w") as file: # Open and use file, this way will automatically close the file once all code in block is complete.
			file.write(content)
		return # complete
	except:
		print("System Error - Failed to save for printing.")
		return

def getOrderProduct():
	"""
	This function will get a "order", the product and its service, and return it.

	Returns:
	order		: List	A list containing the product information, such as name, type, service, and name.
	"""
	print("\nAdd product to order, or exit.\nOptions:")
	print("Gentlemen")
	print("Ladies")

	while True:
		try:
			typ = input("Enter a type or EXIT: ").lower().title()
			if typ == "Exit": # no more products to add
				return "exit"
			elif typ != "Gentlemen" and typ != "Ladies":
				print("Invalid type, try again.")
			else: # valid input
				break # leave loop
		except:
			print("Try again.")

	print("\nOptions:")
	for name, details in PRODUCTS[typ].items(): # loop over every ["name"] = {details} in PRODUCTS global constant.
		if details["type"] == typ:
			print(name)
	
	while True:
		try:
			productName = input("Enter a product name: ").lower().title()
			if PRODUCTS[typ].get(productName) == None: # product name doesn't exist
				print("Not a valid product name, try again.")
			else:
				break
		except:
			print("Try again.")

	print("\nServices available:")
	print(f"Standard: {PRODUCTS[typ][productName]['standard']}")
	print(f"Specialist: {PRODUCTS[typ][productName]['specialist']}")

	while True:
		try:
			service = input("Enter service type: ").lower()
			if service != "standard" and service != "specialist":
				print("Not a valid service, try again.")
			elif PRODUCTS[typ][productName][service] == 0.00: # the service isn't available (£0.00).
				print("This service is not available, try again.")
			else:
				break
		except:
			print("Try again.")
	
	price = PRODUCTS[typ][productName][service]

	if typ == "Gentlemen":
		typ = "Gen"
	else:
		typ = "Lad"

	if service == "standard":
		service = "-st"
	else:
		service = "-sp"
	
	order = [productName, typ, service, price]
	return order

def main():
	"""
	This is the MAIN function used to combine all the above functions, and process any number of orders until shutdown.
	"""
	LONGEST = getLongestItemName(PRODUCTS) # get the longest item name for the global variable - done each time for the case of new products added.

	while True:
		print("Welcome, continue through the next steps to generate order.")
		time.sleep(2)

		products = []
		while True:
			product = getOrderProduct()
			if product == "exit" and len(products) > 0:
				break
			else:
				products.append(product)

		for product in products: # for every arrary within the array of products.
			current = datetime.datetime.now()
			day = str(current.day)
			month = str(current.month)
			year = str(current.year)
			hour = str(current.hour)
			minute = str(current.minute)
			orderNo = day+month+year+hour+minute
			product.append(orderNo) # append created order number

		if len(products) > 0:
			time.sleep(2)
			print("\nPayment Processing")
			time.sleep(1)
			print("Payment Accepted")
			time.sleep(1)
			print("Generating Receipt & Tags")
			
			receipt = createReceipt(LONGEST, products)
			tags = createTag(LONGEST, products)
			saveToFile("receipt.txt", receipt)
			saveToFile("tags.txt", tags)

			time.sleep(1)
			print("\nPrinting Receipt")
			time.sleep(1)
			print("Printing Tags")
			time.sleep(2)
			print("Complete.\n")

		end = input("Press ENTER to continue, or SHUTDOWN to end program: ").lower()
		if end == "shutdown":
			break

	print("Exiting")
	return

main()