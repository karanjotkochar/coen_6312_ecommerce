from models import databasemodel

class Product(object):
    def __init__(self, company_name, product_name, seller_name, category, description, price, availability, size, product_id, rating=[], discounted_price='no discount'):
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
        databasemodel.write(a,'products.json','products')
        print('Product is saved')
        return a
    
    @classmethod
    def get_product(cls,id):
        data=databasemodel.read('products.json')
        products=data['products']
        for p in products:
            if p['product_id']==id:
                return cls(**p)
    
    def filter(type):
        data=databasemodel.read('products.json')
        products=data['products']
        if len(products)>0:
            p=[]
            for i in products:
                if i['category']==type:
                    p.append(i)
            return p
        else:
            print("No products are offered yet")
            return False