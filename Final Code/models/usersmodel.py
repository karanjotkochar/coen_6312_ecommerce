from models import databasemodel
from pprint import pprint
from models.ordermodel import Order
from models.productmodel import Product
from models.cartmodel import Cart
from models.orderhistorymodel import OrderHistory

##################-------------USER CLASS------------########################

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

##################-------------ADMIN CLASS-----------#########################

class Admin(object):
    def __init__(self, id, password, seller_requests):
        self.id=id
        self.password=password
        self.seller_requests=seller_requests
    
    @classmethod
    def get_object(cls):
        data=databasemodel.read('admin.json')
        admin=data['admin'][0]
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
                self.update_admin()
            else:
                print('you have entered wrong input')

    def get_json(self):
        admin={
                "id":self.id,
                "password":self.password,
                "seller_requests":self.seller_requests
                }
        return admin

    def update_admin(self):
        a=self.get_json()
        databasemodel.update_admin(a)
        return True
    
    @staticmethod
    def login(id, password):
        admin=Admin.get_object()
        if (id==admin.id) and (password==admin.password):
            print('Admin Logged in')
            return Admin.get_object()
        else:
            print('Invalid credentials')
    
    @staticmethod
    def logout():
        print("Admin logged out")


################------------SELLER CLASS-------------##############################

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
        data=databasemodel.read('sellers.json')
        sellers=data['sellers']
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
        admin=Admin.get_object()
        admin.seller_requests.append(a)
        admin.update_admin()
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
        databasemodel.write(a,'sellers.json','sellers')
        print('Seller saved successfully')
        return True

    @classmethod
    def find_seller(cls,email):
        data=databasemodel.read('sellers.json')
        sellers=data['sellers']
        for i in sellers:
            if i['email_id']==email:
                return cls(**i)

    def add_product(self):
        p_brand=input('\nenter the product brand\n')
        p_name=input('\nenter product name\n')
        p_seller=input('\nenter your company name\n')
        p_category=input('\nEnter product category (choose from electronics, clothing, accessories, food items)\n')
        p_description=input('\nEnter some product description\n')
        p_price=input('\nEnter the price of product\n')
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
            self.update_seller()
            print('Product added successfully')
            return True
        else:
            print("error adding product")
            return False

    def update_seller(self):
        a=self.get_json()
        databasemodel.update_seller(a)
        return

    def get_json(self):
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
        return a
    
    def remove_product(self):
        data=databasemodel.read('products.json')
        products=data['products']
        if len(self.products_offered)>0:
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
                self.update_seller()
                j=0
                for i in products:
                    if i['product_id']==p:
                        a=products.pop(j)
                        databasemodel.delete_product(a)
                        print('product removed successfully')
                    else:
                        j=j+1
                b=databasemodel.read('buyers.json')
                buyers=b['buyers']
                c=databasemodel.read('carts.json')
                carts=c['carts']
                w=0
                for i in buyers:
                    l=0
                    for j in i['wishlist']:
                        if j==p:
                            print(i['wishlist'].pop(l))
                            databasemodel.update_buyer(b['buyers'].pop(w))
                            break
                        else:
                            l=l+1
                    w=w+1
                for k in carts:
                    m=0
                    for l in k['products']:
                        if l==p:
                            k['products'].pop(m)
                            databasemodel.update_cart(k)
                            break
                        else:
                            m=m+1
                return
            else:
                print('Invalid input')
                return False
        else:
            print("No Products are being offered by you!")
            return False

    def update_product(self):
        if len(self.products_offered)>0:
            print('\nselect the product which you want to update\n')
            k=1
            data=databasemodel.read('products.json')
            products=data['products']
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
                        databasemodel.update_product(m)
                    print('Update Successful')
                    return True
                elif l==2:
                    for m in products:
                        if m['product_id']==self.products_offered[t-1]:
                            m['availability']=j
                        databasemodel.update_product(m)
                    print('Update Successful')
                    return True
                else:
                    print('Invalid Input')
                    return False
            else:
                print('Invalid Input')
                return False
        else:
            print("\nNo Products are being offered by you!\n")
            return False

    def update_details(self):
        i=int(input("\nEnter 1. To update Password 2. To Update years of experience 3. To update account number 4. To update Institution number 5. To update Transit Number\n"))
        if i==1:
            password=input("\nEnter new password")
            self.password=password
            self.update_seller()
            print("\nPassword Updated\n")
            return
        elif i==2:
            exp=input("\nEnter updated value for years of experience\n")
            self.years_of_experience=exp
            self.update_seller()
            print("\nyears of experience updated\n")
            return
        elif i==3:
            acc_number=input("\nEnter new account number\n")
            self.account_number=acc_number
            self.update_seller()
            print("\nAccount number updated")
            return
        elif i==4:
            inst_number=input("\nEnter new Institution number\n")
            self.institution_number=inst_number
            self.update_seller()
            print("\nInstitution number updated\n")
            return
        elif i==5:
            tran_number=input("\nEnter new Transit number\n")
            self.transit_number=tran_number
            self.update_seller()
            print("\nTransit number Updated\n")
            return
        else:
            print("\nInvalid Input\n")
            return
        return

    def order_status(self):
        if len(self.orders)>0:
            print("Which Order's status you want to update?")
            k=1
            for i in self.orders:
                print(f'{k}.  {i}\n')
                k=k+1
            t=int(input('Enter the specific number'))
            p_id=self.orders[t-1]
            o=Order.get_order(p_id)
            d=databasemodel.read('products.json')
            products=d['products']
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
                            o.update_order()
        else:
            print("There are no orders for you yet!\n")
            return

    @staticmethod
    def login(email_id, password):
        data=databasemodel.read('sellers.json')
        sellers=data['sellers']
        if len(sellers)==0:
            print('Seller does not exist')
            return

        elif len(sellers)>0:
            for i in sellers:
                if i['email_id']==email_id:
                    print('Seller exists! Verifying password')
                    if i['password']==password:
                        print('Seller logged in')
                        return Seller.find_seller(email_id)
                    else:
                        print('Wrong Password')
                        return
            print("Seller does not exist")
            return
        else:
            print("Seller does not exist")
            return
                    
    @staticmethod
    def logout():
        print('Seller logged out')

###################----------BUYER CLASS-----------###################################

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
                self.update_buyer()
                print('Item added in wishlist successfully')
                return True
            else:
                print('No more products can be added in the wishlist')
                return False
    
    def view_wishlist(self):
        if len(self.wishlist)>0:
            data=databasemodel.read('products.json')
            products=data['products']
            k=1
            for i in self.wishlist:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}. ')
                        pprint(p)
                        print('\n')
            return
        else:
            print("wishlist is empty!\n")
            return

    def remove_from_wishlist(self):
        if len(self.wishlist)>0:
            print('Which item you want to remove from wishlist')
            k=1
            data= databasemodel.read('products.json')
            products=data['products']
            for i in self.wishlist:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}..')
                        pprint(p)
                        print('\n')
                        k=k+1
            t=int(input('Enter the number for the item you want to remove\n'))
            self.wishlist.pop(t-1)
            self.update_buyer()
            print('Item removed successfully')
            return True
        else:
            print("There are no products in the wishlist\n")
    
    @staticmethod
    def check_for_existance(email_id, phone_number):
        data=databasemodel.read('buyers.json')
        buyers=data['buyers']
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
        data=databasemodel.read('buyers.json')
        buyers=data['buyers']
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
    
    def update_buyer(self):
        data=self.get_json()
        databasemodel.update_buyer(data)
    
    def get_json(self):
        a={'email_id':self.email_id,
            'password':self.password,
            'phone_number':self.phone_number,
            'name':self.name,
            'address':self.address,
            'wishlist':self.wishlist}
        return a
    
    def save(self):
        a={'email_id':self.email_id,
            'password':self.password,
            'phone_number':self.phone_number,
            'name':self.name,
            'address':self.address,
            'wishlist':self.wishlist}
        databasemodel.write(a, 'buyers.json', 'buyers')
        print("Buyer saved successfully")

    def update_information(self):
        t=int(input('Which information you want to update\n1. Update Password\n2. Update Phone Number\n3. Add Address'))
        if t==1:
            new_password=input('Enter New Password')
            self.password=new_password
            self.update_buyer()
            print('Password Updated successfully')
            return True
        elif t==2:
            new_phone_number=input('Enter new phone number')
            data=databasemodel.read('buyers.json')
            buyers=data['buyers']
            for i in buyers:
                if i['phone_number']==new_phone_number:
                    if i['email_id']==self.email_id:
                        print('Phone Number already linked with your account')
                        return False
                    else:
                        print('Phone Number already linked with some other account')
                        return False
            self.phone_number=new_phone_number
            self.update_buyer()
            print('Phone number Updated successfully')
            return True
        elif t==3:
            if len(self.address)<3:
                address=input('Add Address')
                for i in self.address:
                    if i==address:
                        print('Address Entered is already linked with this account')
                        return False
                self.address.append(address)
                self.update_buyer()
                print('Address list Updated successfully')
                return True
            else:
                print('No more new addresses can be added')
                return False
        else:
            print('Incorrect Input')
            return False

    @staticmethod
    def login(email_id, password):
        data=databasemodel.read('buyers.json')
        buyers=data['buyers']
        if len(buyers)==0:
            print('Buyer does not exist')
            return False

        elif len(buyers)>0:
            for i in buyers:
                if i['email_id']==email_id:
                    print('Buyer exists! Verifying password')
                    if i['password']==password:
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
        print('Buyer logged out')
        return True
