from models.productmodel import Product
from models import databasemodel
from pprint import pprint
from datetime import datetime
from models.ordermodel import Order
from models.orderhistorymodel import OrderHistory

class Cart(object):
    def __init__(self,buyer_email, shipping_address, products=[]):
        self.buyer_email=buyer_email
        self.shipping_address=shipping_address
        self.products=products
    
    def add_product(self, p):
        for i in self.products:
            if i==p:
                print('item is already in the cart')
                return False
        if len(self.products)<5:
            a=Product.get_product(p)
            if a.availability=='out of stock':
                print('product is out of stock\n')
            else:
                self.products.append(p)
                self.update_cart()
                print('product added in cart')
                return True
        else:
            print('cart is already full')
            return False
    
    def remove_product(self):
        if len(self.products)>0:
            print('Which item you want to remove from cart')
            k=1
            data= databasemodel.read('products.json')
            products=data['products']
            for i in self.products:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}..')
                        pprint(p)
                        print('\n')
                        k=k+1
            t=int(input('Enter the number for the item you want to remove\n'))
            self.products.pop(t-1)
            self.update_cart()
            print('Item removed successfully')
            return True
        else:
            print("There are no products in the cart\n")
    
    def manage_address(self):
        print(f"Current shipping address is: {self.shipping_address}")
        t=int(input('1. keep this shipping address as it is\n 2. Change shipping address'))
        if t==1:
            print('Shipping address is not changed')
            return True
        elif t==2:
            print('Select new Shipping address\n')
            data=databasemodel.read('buyers.json')
            buyers=data['buyers']
            for i in buyers:
                if i['email_id']==self.buyer_email:
                    k=1
                    for a in i['address']:
                        print(f'{k}. {a}')
                        print('\n')
                        k=k+1
                    sel=int(input('Enter the adress number which you want to set as shipping address'))
                    self.shipping_address=i['address'][sel-1]
                    self.update_cart()
                    print('Shipping address is updated')
                    print(f"New shipping address is: {self.shipping_address}")
                    return True
        else:
            print('wrong input')
            return False

    def place_order(self):
        if len(self.products)>=1:
            print("your cart has these products:\n")
            data=databasemodel.read('products.json')
            products=data['products']
            k=1
            for i in self.products:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}. ')
                        pprint(p)
                        print('\n')
                        k=k+1
            t=input("\ndo you want to continue (yes or no)\n")
            if t=='yes':
                products_ordered=[]
                for i in self.products:
                    products_ordered.append(i)
                buyer_email=self.buyer_email
                status=[]
                for i in self.products:
                    a={'product': i,
                        'status':'in processing'}
                    status.append(a)
                now=datetime.now()
                n=now.strftime("%d/%m/%Y %H:%M:%S")
                a=n.split(' ')
                b=a[1].split(':')
                c=b[0]+'-'+b[1]+'-'+b[2]
                order_id=self.buyer_email+'-'+a[0]+'@'+c
                order_placed=Order.create_order(order_id, products_ordered, status, buyer_email)
                a=OrderHistory.get_order_history(buyer_email)
                a.orders.append(order_placed['order_id'])
                a.update_order_history()
                self.products.clear()
                self.update_cart()
                print('Order Placed Successfully')
                return True
            else:
                print('\nOrder not placed\n')
                return False
        else:
            print('The cart is empty, NO order can be placed')
            return False

    def get_json(self):
        a={'buyer_email':self.buyer_email,
            'shipping_address':self.shipping_address,
            'products':self.products}
        return a
    
    def update_cart(self):
        data= self.get_json()
        databasemodel.update_cart(data)
        return True
    
    def save(self):
        a={'buyer_email':self.buyer_email,
            'shipping_address':self.shipping_address,
            'products':self.products}
        databasemodel.write(a, 'carts.json', 'carts')
        return True

    @classmethod
    def get_cart(cls,email):
        data= databasemodel.read('carts.json')
        carts=data['carts']
        for i in carts:
            if i['buyer_email']==email:
                return cls(**i)
