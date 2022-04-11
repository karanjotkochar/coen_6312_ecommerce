from models import databasemodel
from pprint import pprint

class OrderHistory(object):
    def __init__(self, buyer_email, orders=[]):
        self.buyer_email=buyer_email
        self.orders=orders
    
    def view_orders(self):
        data=databasemodel.read('orders.json')
        orders=data['orders']
        for i in self.orders:
            for o in orders:
                if i==o['order_id']:
                    pprint(o)
                    print('\n')
    
    def get_json(self):
        a={'buyer_email':self.buyer_email,
            'orders':self.orders}
        return a

    def update_order_history(self):
        data=self.get_json()
        databasemodel.update_order_history(data)
        return True
    
    def save(self):
        a={'buyer_email':self.buyer_email,
            'orders':self.orders}
        databasemodel.write(a, 'orderhistory.json', 'order_history')
        return

    @classmethod
    def get_order_history(cls,email):
        data=databasemodel.read('orderhistory.json')
        order_history=data['order_history']
        for i in order_history:
            if i['buyer_email']==email:
                return cls(**i)