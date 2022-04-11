from models import databasemodel
from pprint import pprint

class Order(object):
    def __init__(self, order_id, products, status, buyer_email):
        self.order_id=order_id
        self.products=products
        self.status=status
        self.buyer_email=buyer_email

    @staticmethod
    def create_order(order_id, products_ordered, status, buyer_email):
        o=Order(order_id, products_ordered, status, buyer_email)
        data=databasemodel.read('products.json')
        products=data['products']
        data1=databasemodel.read('sellers.json')
        sellers=data1['sellers']
        for p in o.products:
            for z in products:
                if z['product_id']==p:
                    for i in sellers:
                        if i['company_name']==z['seller_name']:
                            i['orders'].append(o.order_id)
                            databasemodel.update_seller(i)
        return o.save()
    
    def save(self):
        a={'order_id':self.order_id,
            'products':self.products,
            'status':self.status,
            'buyer_email':self.buyer_email}
        databasemodel.write(a, 'orders.json', 'orders')
        return a
    
    def get_json(self):
        a={'order_id':self.order_id,
            'products':self.products,
            'status':self.status,
            'buyer_email':self.buyer_email}
        return a
    
    def update_order(self):
        data=self.get_json()
        databasemodel.update_order(data)
    
    def check_status(self):
        k=1
        data=databasemodel.read('products.json')
        products=data['products']
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
            data=databasemodel.read('products.json')
            products=data['products']
            for i in cancelation_allowed:
                for p in products:
                    if p['product_id']==i:
                        print(f'{k}. (Order ID:- {i}) {p}')
                        print('\n')
                        k=k+1
            t=int(input('Enter the specific number'))
            to_be_cancel=cancelation_allowed[t-1]
            for i in self.status:
                if i['product']==to_be_cancel:
                    i['status']='order cancelled'
                    self.update_order()
    
    def add_rating(self):
        can_be_rated=[]
        for i in self.status:
            if i['status']=='delivered':
                can_be_rated.append(i['product'])
        if len(can_be_rated)==0:
            print('currently you cannot rate products purchased under this order')
        else:
            k=1
            data=databasemodel.read('products.json')
            products=data['products']
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
                    databasemodel.update_product(i)
                    return True

    @classmethod
    def get_order(cls,id):
        data=databasemodel.read('orders.json')
        orders=data['orders']
        for i in orders:
            if i['order_id']==id:
                return cls(**i)
