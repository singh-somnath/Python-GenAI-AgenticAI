class Grocerry:
    def __init__(self):
        self.cart = {}
        self.items = {
            "Milk":45,
            "Rice":60,
            "Bread":50,
            "Potato":30,
            "Onion":50,
            "Garlic":80,
            "Lemon":10    
        }
    
    def availableItems(self):
        print("-----------------Available Items ----------------")
        print('|'.join(f"{item} : {price}" for item, price in self.items.items()))

    def addItemsInCart(self,item,quantity):
        if item in self.items.keys():
            self.cart[item] = quantity
        else:
            print(f"{item} not available")        
    
    def removeItemFromCart(self,item):
        if item in self.cart.keys():
            item = self.cart.pop(item,None)
            print(f"{item} has deleted from cart")
        else:
            print(f"{item} is not present in cart")
    
    def calculatePrice(self):
        if len(self.cart) > 0:
            return  sum(self.items[item] * quantity  for item,quantity in self.cart.items())
        else:
            print(f"Cart is empty")
    
    def checkout(self):
        if len(self.cart) > 0:
            print("Your cart:")
            print(("\n").join([item + " " + str(quantity) for item,quantity in self.cart.items()]))
            print(f"Total Price - {self.calculatePrice()}")
        else:
            print("Cart is empty")
        
        print("Thank you!")


grocerry = Grocerry()

while True:
    print("==================Welcome to Grocerry Store====================")  
    userInput = input("Please provide your input [Available Items - 1 | Add Item - 2 | Remove Item - 3 | Calculate Price - 4 |Checkout -5] : ")
    try:
        userInput = int(userInput)
    except Exception as e:
        print(e)
        continue

    if userInput == 1:
        grocerry.availableItems()
    elif userInput == 2 :
        item = input("Enter item name : ").strip()
        quantity = int(input("Enter Quantity : ").strip())
        grocerry.addItemsInCart(item,quantity)
    elif userInput == 3  :
        item = input("Enter item to remove : ").strip()      
        grocerry.removeItemFromCart(item)
    elif userInput == 4  :
        print(f"Total Price : {grocerry.calculatePrice()}")
    elif userInput == 5  :      
        grocerry.checkout()
        break

       

    