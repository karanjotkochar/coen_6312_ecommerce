from pprint import pprint
from models.ordermodel import Order
from models.productmodel import Product
from models.cartmodel import Cart
from models.orderhistorymodel import OrderHistory
from models.usersmodel import Admin, Buyer, Seller
from models import databasemodel

i=1

while i==1:
    
    z=int(input('\nEnter\n1. To Continue as Admin\n2. To Continue as Seller\n3. To Continue as Buyer\n0. To Exit\n'))
    
    if z==1:
        x=1
        while x==1:
            j=int(input('\nEnter\n1. To Login\n0. To go back to previous menu\n'))
            if j==1:
                id=input("\nEnter Admin id (id is admin)\n")
                password=input("\nEnter Admin password (password is admin)\n")
                a=Admin.login(id, password)
                if a:
                    y=1
                    while y==1:
                        m=int(input("\nEnter\n1. To Approve Seller Requests\n2. To Logout\n"))
                        if m==1:
                            a.verify_sellers()
                        elif m==2:
                            a.logout()
                            y=0
            elif j==0:
                x=0
    elif z==2:
        x=1
        while x==1:
            j=int(input("\nEnter\n1. To Login\n2. To submit signup request\n3. To go back to previous menu\n"))
            if j==1:
                email=input("\nEnter Email\n")
                password=input("\nEnter password\n")
                a= Seller.login(email, password)
                if a:
                    y=1
                    while y==1:
                        m=int(input("\nEnter\n1. To add product\n2. To remove product\n3. Update any Product\n4. To update Order Status\n5. To Update your details\n6. To Logout"))
                        if m==1:
                            a.add_product()
                        elif m==2:
                            a.remove_product()
                        elif m==3:
                            a.update_product()
                        elif m==4:
                            a.order_status()
                        elif m==5:
                            a.update_details()
                        elif m==6:
                            a.logout()
                            y=0
            elif j==2:
                email_id=input("\nEnter Email id\n")
                password=input("\nEnter password\n")
                phone_number=input("\nEnter Phone Number\n")
                company_name=input("\nEnter Company Name\n")
                business_address=input("\nEnter Business Address\n")
                years_of_experience=input("\nEnter years of experience\n")
                account_number=input("\nEnter account number\n")
                institution_number=input("\nEnter institution number\n")
                transit_number=input("\nEnter transit number\n")
                Seller.request_signup(email_id, password, phone_number, company_name, business_address, years_of_experience, account_number, institution_number, transit_number)
            
            elif j==3:
                x=0
    elif z==3:
        x=1
        while x==1:
            j=int(input("\nEnter\n1. To Signup as Buyer\n2. To Login as Buyer\n3. To go back to previous menu\n"))
            if j==1:
                email_id=input("\nEnter email id\n")
                password=input("\nEnter password\n")
                phone_number=input("\nEnter Phone Number\n")
                name=input("\nEnter Name\n")
                address=input("\nEnter your address\n")
                Buyer.signup(email_id,password,phone_number,name,address)
            if j==2:
                email_id=input("\nEnter email id\n")
                password=input("\nEnter password\n")
                a=Buyer.login(email_id, password)
                if a:
                    y=1
                    while y==1:
                        m=int(input("\nEnter\n1. To add product to wishlist\n2. To view wishlist\n3. To update your information\n4. To add product to your cart\n5. To remove product from your cart\n6. To manage your shipping address\n7. To Place Order for items in the cart\n8. To view Order History (To check order status, cancel order or add rating for purchased products)\n9. To remove item from wishlist\n10. To Logout\n"))
                        if m==1:
                            print("Products are offered in the following categories\n")
                            g=int(input("Enter\n1. For Electronics\n2. For Clothing\n3. For accessories\n4. For Food Items\n"))
                            if g==1:
                                p=Product.filter('electronics')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to wishlist"))
                                        id=p.pop(w-1)
                                        a.add_to_wishlist(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==2:
                                p=Product.filter('clothing')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to wishlist"))
                                        id=p.pop(w-1)
                                        a.add_to_wishlist(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==3:
                                p=Product.filter('accessories')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to wishlist"))
                                        id=p.pop(w-1)
                                        a.add_to_wishlist(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==4:
                                p=Product.filter('food items')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to wishlist"))
                                        id=p.pop(w-1)
                                        a.add_to_wishlist(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            else:
                                print("Invalid Input\n")
                        elif m==2:
                            a.view_wishlist()
                        elif m==3:
                            a.update_information()
                        elif m==4:
                            c=Cart.get_cart(a.email_id)
                            print("Products are offered in the following categories\n")
                            g=int(input("Enter\n1. For Electronics\n2. For Clothing\n3. For accessories\n4. For Food Items\n"))
                            if g==1:
                                p=Product.filter('electronics')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to your cart"))
                                        id=p.pop(w-1)
                                        c.add_product(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==2:
                                p=Product.filter('clothing')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to your cart"))
                                        id=p.pop(w-1)
                                        c.add_product(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==3:
                                p=Product.filter('accessories')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to your cart"))
                                        id=p.pop(w-1)
                                        c.add_product(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            elif g==4:
                                p=Product.filter('food items')
                                if p:
                                    if len(p)>0:
                                        s=1
                                        for d in p:
                                            print(f'\n{s}. ')
                                            pprint(d)
                                            print('\n')
                                            s=s+1
                                        w=int(input("Enter the product number which you want to add to your cart"))
                                        id=p.pop(w-1)
                                        c.add_product(id['product_id'])
                                else:
                                    print("No products are offered under this category\n")
                            else:
                                print("Invalid Input\n")
                        elif m==5:
                            u=Cart.get_cart(a.email_id)
                            u.remove_product()
                        elif m==6:
                            v=Cart.get_cart(a.email_id)
                            v.manage_address()
                        elif m==7:
                            qq=Cart.get_cart(a.email_id)
                            qq.place_order()
                        elif m==8:
                            o=OrderHistory.get_order_history(a.email_id)
                            r=int(input("\nEnter\n1. To view Orders placed and their status\n2. To Cancel Order\n3. To add rating\n"))
                            if r==1:
                                if len(o.orders)>0:
                                    data=databasemodel.read('orders.json')
                                    orders=data['orders']
                                    for d in o.orders:
                                        for u in orders:
                                            if u['order_id']==d:
                                                pprint(u)
                                else:
                                    print("No orders are placed yet!\n")
                            if r==2:
                                if len(o.orders)>0:
                                    data=databasemodel.read('orders.json')
                                    orders=data['orders']
                                    q=1
                                    for d in o.orders:
                                        for u in orders:
                                            if u['order_id']==d:
                                                print(f'{q}. ')
                                                pprint(u)
                                                print('\n')
                                                q=q+1
                                    f=int(input("\nEnter the specific order for which you want to make cancellation\n"))
                                    id=o.orders[f-1]
                                    b=Order.get_order(id)
                                    b.cancel_order()
                                else:
                                    print("No orders are placed yet!\n")
                            if r==3:
                                if len(o.orders)>0:
                                    data=databasemodel.read('orders.json')
                                    orders=data['orders']
                                    q=1
                                    for d in o.orders:
                                        for u in orders:
                                            if u['order_id']==d:
                                                print(f'{q}. ')
                                                pprint(u)
                                                print('\n')
                                                q=q+1
                                    f=int(input("\nEnter the specific order for which you want to add rating\n"))
                                    id=o.orders[f-1]
                                    b=Order.get_order(id)
                                    b.add_rating()
                                else:
                                    print("No orders are placed yet!\n")
                        elif m==9:
                            a.remove_from_wishlist()
                        elif m==10:
                            a.logout()
                            y=0
            if j==3:
                x=0
    elif z==0:
        i=0

