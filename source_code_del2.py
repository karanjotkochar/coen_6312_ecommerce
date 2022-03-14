from datetime import datetime
from pprint import pprint

buyers=[]
sellers=[]
carts=[]
products=[]
admin={'id':'admin','password':'admin','seller_requests':[]}
order_history=[]
person=[]
orders=[]

#----------------------------------------USER CLASS--------------------------------


class User(object):

    def __init__(self, email_id, password, phone_number):
        self.email_id=email_id
        self.password=password
        self.phone_number=phone_number

    @staticmethod
    def login():
        pass

    @staticmethod
    def logout():
        pass


#-----------------------PRODUCT CLASS------------------------------------


class Product(object):
    def __init__(self, company_name, product_name, seller_name, category, description, price, availability, size, product_id, rating=[], discounted_price=float):
        self.company_name=company_name
        self.product_name=product_name
        self.seller_name=seller_name
        self.category=category
        self.description=description
        self.price=price
        self.availability=availability
        self.size=size
        self.rating=rating
        self.discounted_price=discounted_price
        self.product_id=product_id
    
    @staticmethod
    def create_product(company_name, product_name, seller_name, category, description, price, availability, size, product_id):
        p=Product(company_name, product_name, seller_name, category, description, price, availability, size, product_id)
        b= p.save()
        print('Product is added')
        return b

    def save(self):
        a={'company_name':self.company_name,
            'product_name':self.product_name,
            'seller_name':self.seller_name,
            'category':self.category,
            'description':self.description,
            'price':self.price,
            'availability':self.availability,
            'size':self.size,
            'product_id':self.product_id,
            'rating':self.rating,
            'discounted_price':self.discounted_price}
        products.append(a)
        print('Product is saved')
        return a
    
    @classmethod
    def get_product(cls,id):
        for p in products:
            if p['product_id']==id:
                return cls(**p)
    
    def filter():
        pass
        #to be implemented later


#-----------------------------------ORDER HISTORY CLASS-------------------


class OrderHistory(object):
    def __init__(self, buyer_email, orders=[]):
        self.buyer_email=buyer_email
        self.orders=orders
    
    def view_orders(self):
        for i in self.orders:
            for o in orders:
                if i==o['order_id']:
                    pprint(o)
                    print('\n')
    
    def save(self):
        a={'buyer_email':self.buyer_email,
            'orders':self.orders}
        order_history.append(a)

    @classmethod
    def get_order_history(cls,email):
        for i in order_history:
            if i['buyer_email']==email:
                return cls(**i)


#------------------------------------ORDER CLASS------------------------------


class Order(object):
    def __init__(self, order_id, products, status, buyer_email):
        self.order_id=order_id
        self.products=products
        self.status=status
        self.buyer_email=buyer_email

    @staticmethod
    def create_order(order_id, products_ordered, status, buyer_email):
        o=Order(order_id, products_ordered, status, buyer_email)
        for p in o.products:
            for z in products:
                if z['product_id']==p:
                    for i in sellers:
                        if i['company_name']==z['seller_name']:
                            i['orders'].append(o.order_id)
        return o.save()
    
    def save(self):
        a={'order_id':self.order_id,
            'products':self.products,
            'status':self.status,
            'buyer_email':self.buyer_email}
        orders.append(a)
        return a
    
    def check_status(self):
        k=1
        for i in self.status:
            for p in products:
                if i['product']==p['product_id']:
                    print(k)
                    pprint(i)
                    pprint(p)
                    print('\n')
                    k=k+1
    
    def cancel_order(self):
        cancelation_allowed=[]
        for i in self.status:
            if i['status']=='in processing':
                cancelation_allowed.append(i['product'])
        
        if len(cancelation_allowed)==0:
            print('you cannot cancel your order now')
        else:
            print('which product you want to cancel')
            k=1
            for i in cancelation_allowed:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}. {i}')
                        print('\n')
                        k=k+1
            t=int(input('Enter the specific number'))
            to_be_cancel=cancelation_allowed[t-1]
            for i in self.status:
                if i['product']==to_be_cancel:
                    i['status']='order cancelled'
    
    def add_rating(self):
        can_be_rated=[]
        for i in self.status:
            if i['status']=='delivered':
                can_be_rated.append(i['product'])
        if len(can_be_rated)==0:
            print('currently you cannot rate products purchased under this order')
        else:
            k=1
            print('select product which you want to rate')
            for i in can_be_rated:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}... {p}')
                        print('\n')
                        k=k+1
            t=int(input('give the specific product number which you want to rate'))
            to_rate=can_be_rated[t-1]
            r=int(input('Enter the rating (integer value) on 5 point scale'))
            for i in products:
                if i['product_id']==to_rate:
                    i['rating'].append(r)

    @classmethod
    def get_order(cls,id):
        for i in orders:
            if i['order_id']==id:
                return cls(**i)


#---------------------------------------CART CLASS--------------------------------------------


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
                print('product added in cart')
                return True
        else:
            print('cart is already full')
            return False
    
    def remove_product(self):
        print('Which item you want to remove from cart')
        k=1
        for i in self.products:
            for p in products:
                if p['product_id']==i:
                    print(f'{k}..')
                    pprint(p)
                    print('\n')
                    k=k+1
        t=int(input('Enter the number for the item you want to remove\n'))
        self.products.pop(t-1)
        print('Item removed successfully')
        return True
    
    def manage_address(self):
        print(f"Current shipping address is: {self.shipping_address}")
        t=int(input('1. keep this shipping address as it is\n 2. Change shipping address'))
        if t==1:
            print('Shipping address is not changed')
            return True
        elif t==2:
            print('Select new Shipping address\n')
            for i in buyers:
                if i['email_id']==self.buyer_email:
                    k=1
                    for a in i['address']:
                        print(f'{k}. {a}')
                        print('\n')
                        k=k+1
                    sel=int(input('Enter the adress number which you want to set as shipping address'))
                    self.shipping_address=i['address'][sel-1]
                    print('Shipping address is updated')
                    return True
        else:
            print('wrong input')
            return False

    def place_order(self):
        if len(self.products)>=1:
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
            for i in order_history:
                if i['buyer_email']==self.buyer_email:
                    i['orders'].append(order_placed['order_id'])
            self.products.clear()
            print('Order Placed Successfully')
            return True
        else:
            print('The cart is empty, NO order can be placed')

    def save(self):
        a={'buyer_email':self.buyer_email,
            'shipping_address':self.shipping_address,
            'products':self.products}
        carts.append(a)

    @classmethod
    def get_cart(cls,email):
        for i in carts:
            if i['buyer_email']==email:
                return cls(**i)


#--------------------------------------BUYER CLASS---------------------------------


class Buyer(User):
    def __init__(self, email_id, password, phone_number, name, address, wishlist=[]):
        super().__init__(email_id, password, phone_number)
        self.name=name
        self.address=address
        self.wishlist=wishlist
    
    
    def add_to_wishlist(self, p):
        for i in self.wishlist:
            if i==p:
                print("product is already added in wishlist")
                return False
        else:
            if len(self.wishlist)<10:
                self.wishlist.append(p)
                print('Item added in wishlist successfully')
                return True
            else:
                print('No more products can be added in the wishlist')
                return False
    
    @staticmethod
    def check_for_existance(email_id, phone_number):
        if len(buyers)==0:
            return True
        else:
            for i in buyers:
                if i['email_id']==email_id or i['phone_number']==phone_number:
                    print('Buyer already exists')
                    return False
            return True
    
    @classmethod
    def find_buyer(cls,email):
        for i in buyers:
            if i['email_id']==email:
                return cls(**i)
    

    @staticmethod
    def signup(email_id, password, phone_number, name, address):
        check=Buyer.check_for_existance(email_id, phone_number)
        if check:
            add=[]
            add.append(address)
            b=Buyer(email_id, password, phone_number, name, add)
            b.save()
            c=Cart(email_id, add[0])
            c.save()
            o=OrderHistory(email_id)
            o.save()
            print('Buyer Signed up successfully')
            return True
        else:
            return False

    def save(self):
        a={'email_id':self.email_id,
            'password':self.password,
            'phone_number':self.phone_number,
            'name':self.name,
            'address':self.address,
            'wishlist':self.wishlist}
        buyers.append(a)
        print("Buyer saved successfully")

    def update_information(self):
        t=int(input('Which information you want to update\n1. Update Password\n2. Update Phone Number\n3. Add Address'))
        if t==1:
            new_password=input('Enter New Password')
            self.password=new_password
            print('Password Updated successfully')
            return True
            #for i in buyers:
            #    if i['email_id']==a.email_id:
            #        i['password']=a.password
            #        print('Password Updated successfully')
            #        return True
        elif t==2:
            new_phone_number=input('Enter new phone number')
            for i in buyers:
                if i['phone_number']==new_phone_number:
                    if i['email_id']==self.email_id:
                        print('Phone Number already linked with your account')
                        return False
                    else:
                        print('Phone Number already linked with some other account')
                        return False
            self.phone_number=new_phone_number
            print('Phone number Updated successfully')
            return True
            #for i in buyers:
            #    if i['email_id']==a.email_id:
            #        i['phone_number']=a.phone_number
            #        print('Phone number Updated successfully')
            #        return True
        elif t==3:
            if len(self.address)<3:
                address=input('Add Address')
                for i in self.address:
                    if i==address:
                        print('Address Entered is already linked with this account')
                        return False
                self.address.append(address)
                print('Address list Updated successfully')
                return True
                #for i in buyers:
                #    if i['email_id']==a.email_id:
                #        i['address']=a.address
                #        print('Address list Updated successfully')
                #        return True
            else:
                print('No more new addresses can be added')
                return False
        else:
            print('Incorrect Input')
            return False

    @staticmethod
    def login(email_id, password):
        if len(buyers)==0:
            print('Buyer does not exist')
            return False

        elif len(buyers)>0:
            for i in buyers:
                if i['email_id']==email_id:
                    print('Buyer exists! Verifying password')
                    if i['password']==password:
                        person.append(i['email_id'])
                        print('Buyer logged in')
                        return Buyer.find_buyer(email_id)
                    else:
                        print('Wrong Password')
                        return False
        else:
            print("Buyer does not exist")
            return False
                    
    @staticmethod
    def logout():
        person.pop(0)
        print('Buyer logged out')
        return True


#-------------------------------------------SELLER CLASS--------------------------------------------


class Seller(User):
    def __init__(self, email_id, password, phone_number, company_name, business_address, years_of_experience, account_number, institution_number, transit_number, products_offered=[], orders=[]):
        super().__init__(email_id, password, phone_number)
        self.company_name=company_name
        self.business_address=business_address
        self.years_of_experience=years_of_experience
        self.account_number=account_number
        self.transit_number=transit_number
        self.institution_number=institution_number
        self.products_offered=products_offered
        self.orders=orders
    
    @staticmethod
    def request_signup(email_id, password, phone_number, company_name, business_address, years_of_experience, account_number, institution_number, transit_number):
        if len(sellers)>0:
            for i in sellers:
                if i['email_id']==email_id or i['phone_number']==phone_number or i['company_name']==company_name or i['business_address']==business_address:
                    print('Seller already existed! Request Denied')
                    return False
        a={'email_id':email_id,
            'password':password,
            'phone_number':phone_number,
            'company_name':company_name,
            'business_address':business_address,
            'years_of_experience':years_of_experience,
            'account_number':account_number,
            'institution_number':institution_number,
            'transit_number':transit_number}
        admin['seller_requests'].append(a)
        print("sign up request received")
        return True

    @staticmethod
    def approve_request(email_id, password, phone_number, company_name, business_address, years_of_experience, account_number, institution_number, transit_number):
        s=Seller(email_id, password, phone_number, company_name, business_address, years_of_experience, account_number, institution_number, transit_number)
        s.save()
        print('seller registered successfully')
        return True
    
    def save(self):
        a={'email_id':self.email_id,
            'password':self.password,
            'phone_number':self.phone_number,
            'company_name':self.company_name,
            'business_address':self.business_address,
            'years_of_experience':self.years_of_experience,
            'account_number':self.account_number,
            'institution_number':self.institution_number,
            'transit_number':self.transit_number,
            'products_offered':self.products_offered,
            'orders':self.orders}
        sellers.append(a)
        print('Seller saved successfully')
        return True

    @classmethod
    def find_seller(cls,email):
        for i in sellers:
            if i['email_id']==email:
                return cls(**i)

    def add_product(self):
        p_brand=input('\nenter the product brand\n')
        p_name=input('\nenter product name\n')
        p_seller=input('\nenter your company name\n')
        p_category=input('\nEnter product category (choose from electronics, clothing, accessories, food items)\n')
        p_description=input('\nEnter some product description\n')
        p_price=float(input('\nEnter the price of product\n'))
        p_availability=input('\nEnter product availability i.e. Whether it is "in stock", "will be out soon" or "out of  stock"\n')
        p_size=input('\nEnter product size/weight whatever is applicable\n')
        p_id= p_brand + p_name + p_seller + p_size
        p_id=p_id.upper()
        for i in self.products_offered:
            if i==p_id:
                print('This product is already offered by you')
                return False
        a=Product.create_product(p_brand, p_name,p_seller,p_category, p_description, p_price, p_availability, p_size, p_id)
        if a:
            self.products_offered.append(a['product_id'])
            print('Product added successfully')
            return True
        else:
            print("error adding product")
            return False

    def remove_product(self):
        print('select the product which you want to remove')
        k=1
        for i in self.products_offered:
            for p in products:
                if i==p['product_id']:
                    print(f'{k}.....')
                    pprint(p)
                    print('\n')
                    k=k+1
        t=int(input('Enter the specific number'))
        if t<=len(self.products_offered):
            p=self.products_offered.pop(t-1)
            j=0
            for i in products:
                if i['product_id']==p:
                    products.pop(j)
                    print('product removed successfully')
                    return True
                else:
                    j=j+1
            for i in buyers:
                for j in i['wishlist']:
                    if j==p:
                        i['wishlist'].remove(j)
                for k in carts:
                    if k['buyer_email']==i['email_id']:
                        for l in k['products']:
                            if l==p:
                                k['products'].remove(l)
        else:
            print('Invalid input')
            return False

    def update_product(self):
        print('\nselect the product which you want to update\n')
        k=1
        for i in self.products_offered:
            for p in products:
                if i==p['product_id']:
                    print(f'{k}.....')
                    pprint(p)
                    print('\n')
                    k=k+1
        t=int(input('Enter the specific number'))
        if t<=len(self.products_offered):
            for z in products:
                if z['product_id']==self.products_offered[t-1]:
                    pprint(z)
                    print('\n')
            l=int(input('\nSelect 1 if you want to update the price or 2 if you want to update the availability'))
            j=input('\nEnter the value: ')
            if l==1:
                for m in products:
                    if m['product_id']==self.products_offered[t-1]:
                        m['price']=j
                print('Update Successful')
                return True
            elif l==2:
                for m in products:
                    if m['product_id']==self.products_offered[t-1]:
                        m['availability']=j
                print('Update Successful')
                return True
            else:
                print('Invalid Input')
                return False
        else:
            print('Invalid Input')
            return False

    def update_details(self):
        pass

    def order_status(self):
        print("Which Order's status you want to update?")
        k=1
        for i in self.orders:
            print(f'{k}.  {i}\n')
            k=k+1
        t=int(input('Enter the specific number'))
        p_id=self.orders[t-1]
        o=Order.get_order(p_id)
        for i in o.status:
            if i['status']=='in processing' or i['status']=='shipped':
                p=Product.get_product(i['product'])
                if p.seller_name==self.company_name:
                    for y in products:
                        if y['product_id']==p.product_id:
                            pprint(y)
                    print(f"The current status is {i['status']}\n")
                    s=input('Enter the updated status or press 0 if you do not want to update')
                    if s=='0':
                        continue
                    else:
                        i['status']=s

    @staticmethod
    def login(email_id, password):
        if len(sellers)==0:
            print('Seller does not exist')
            return

        elif len(sellers)>0:
            for i in sellers:
                if i['email_id']==email_id:
                    print('Seller exists! Verifying password')
                    if i['password']==password:
                        person.append(i['email_id'])
                        print('Seller logged in')
                        return Seller.find_seller(email_id)
                    else:
                        print('Wrong Password')
                        return
        else:
            print("Seller does not exist")
                    
    @staticmethod
    def logout():
        person.pop(0)
        print('Seller logged out')


#-------------------------------------------------ADMIN CLASS----------------------------------


class Admin(object):
    def __init__(self, id, password, seller_requests):
        self.id=id
        self.password=password
        self.seller_requests=seller_requests
    
    @classmethod
    def get_object(cls):
        return cls(**admin)
    
    def verify_sellers(self):
        if(len(self.seller_requests))==0:
            print('there are no pending requests')
        else:
            print('Select the seller request which you want to approve\n')
            k=1
            for i in self.seller_requests:
                print(f'{k}. {i}\n')
                k=k+1
            t=int(input('Which request you want to approve? (Enter 0 if None)\n'))
            if t==0:
                return
            elif t<=len(self.seller_requests):
                s=self.seller_requests.pop(t-1)
                Seller.approve_request(s['email_id'], s['password'], s['phone_number'], s['company_name'], s['business_address'], s['years_of_experience'], s['account_number'], s['institution_number'], s['transit_number'])
                admin['seller_requests']=self.seller_requests
            else:
                print('you have entered wrong input')

    @staticmethod
    def login(id, password):
        if (id==admin['id']) and (password==admin['password']):
            print('Admin Logged in')
            person.append(id)
            return Admin.get_object()
        else:
            print('Invalid credentials')
    
    @staticmethod
    def logout():
        person.pop(0)
        print("Admin logged out")


print('This is the demo implementation of all the classes and their functionality\n')
print('First we are putting a seller registration request\n')
Seller.request_signup('abc@abc.com', '123456', '4389269055', 'navdeep feed store', '1436 rue Mackay', '2', '4102565', '110', '001')
print('We are displaying the admin object which contains the seller registration request\n')
pprint(admin)
input('Now the admin will login to approve the seller request (press Enter Key to continue)\n')
id=input("Enter Admin login id (id is 'admin' please enter)\n")
password=input("Enter admin password (password is 'admin' please enter)\n")
z=Admin.login(id, password)
z.verify_sellers()
print('Displaying the sellers in the system\n')
pprint(sellers)
print('Displaying admin object now to show that now there are no seller requests pending\n')
pprint(admin)
z.logout()
print('Now the seller is logging in to add products, please enter the required inputs\n')
a=Seller.login('abc@abc.com','123456')
a.add_product()
print('Displaying seller details now to show that product has been added\n')
pprint(sellers)
print('Displaying all products in the system\n')
pprint(products)
print('\nAdding one more product, please enter the required inputs\n')
a.add_product()
print('Displaying sellers and products once again\n')
pprint(sellers)
pprint(products)
print('\nAdding one more product, please enter the required inputs\n')
a.add_product()
print('Displaying sellers and products once again\n')
pprint(sellers)
pprint(products)
print('Lets say the seller wants to update the product\n')
a.update_product()
print('Displaying the seller and products to confirm the changes done')
pprint(sellers)
pprint(products)
print('Seller is logging out now\n')
a.logout()
print('\n Buyer Signing Up\n')
Buyer.signup('singhnavdeep447@gmail.com','123456','4389269055','Navdeep Singh','1436 rue Mackay')
print('Buyer logging in\n')
b=Buyer.login('singhnavdeep447@gmail.com','123456')
c=Cart.get_cart(b.email_id)
o=OrderHistory.get_order_history(b.email_id)
print('\nDisplaying Cart Object of buyer\n')
for k in carts:
    if k['buyer_email']==b.email_id:
        pprint(k)
        print('\n')
print('Displaying Order History object of buyer\n')
for x in order_history:
    if x['buyer_email']==b.email_id:
        pprint(x)
        print('\n')
print('Buyer want to add product in wishlist \n')
print('Which product you want to add\n')
q=1
for p in products:
    print(q)
    pprint(p)
    print('\n')
    q=q+1
e=int(input('Enter the specific number'))
b.add_to_wishlist(products[e-1]['product_id'])
print('Displaying Buyer to confirm that item is added in wishlist\n')
for d in buyers:
    d['email_id']==b.email_id
    pprint(d)
    print('\n')
print('Buyer want to add product in cart \n')
print('Which product you want to add\n')
q=1
for p in products:
    print(q)
    pprint(p)
    print('\n')
    q=q+1
e=int(input('Enter the specific number'))
c.add_product(products[e-1]['product_id'])
print('Displaying cart object to confirm\n')
for k in carts:
    if k['buyer_email']==b.email_id:
        pprint(k)
        print('\n')
print('\n Buyer wants to update information, lets say add new address\n')
b.update_information()
print('Buyer to change shipping address\n')
c.manage_address()
print('Buyer wants to place order\n')
c.place_order()
print('Displaying cart object now to view shipping address which we updated, products in cart should be empty now as an order is placed\n')
for k in carts:
    if k['buyer_email']==b.email_id:
        pprint(k)
        print('\n')
print('Displaying order history object now\n')
for x in order_history:
    if x['buyer_email']==b.email_id:
        pprint(x)
        print('\n')
print('buyer logging out\n')
print('seller logging in\n')
a=Seller.login('abc@abc.com','123456')
print('displaying seller object now to see the order id in orders for seller')
pprint(sellers)
print('Lets say seller want to remove some product now\n')
a.remove_product()
print('Displaying products now to confirm change\n')
pprint(products)
print('\n')
print('Lets say seller wants to update the status of order\n')
a.order_status()
print('Displaying orders to confirm change\n')
pprint(orders)
print('Selelr logging out\n')
a.logout()
