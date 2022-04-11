import json



def write(data, f, context):
    content=read(f)
    content[context].append(data)
    a="dbfiles/"
    filename=a+f
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)


def read(f):
    a="dbfiles/"
    filename=a+f
    with open(filename) as json_file:
        data= json.load(json_file)
        return data

def update_admin(data):
    data1=read('admin.json')
    data1['admin'].pop(0)
    data1['admin'].append(data)
    with open('dbfiles/admin.json', "w") as f:
        json.dump(data1, f, indent=4)

def update_seller(data):
    data1=read('sellers.json')
    i=0
    for s in data1['sellers']:
        if s['email_id']==data['email_id']:
            data1['sellers'].pop(i)
        else:
            i=i+1
    data1['sellers'].append(data)
    with open('dbfiles/sellers.json', "w") as f:
        json.dump(data1,f,indent=4)

def update_product(data):
    data1=read('products.json')
    i=0
    for p in data1['products']:
        if p['product_id']==data['product_id']:
            data1['products'].pop(i)
        else:
            i=i+1
    data1['products'].append(data)
    with open('dbfiles/products.json',"w") as f:
        json.dump(data1, f, indent=4)

def update_buyer(data):
    data1=read('buyers.json')
    i=0
    for b in data1['buyers']:
        if b['email_id']==data['email_id']:
            data1['buyers'].pop(i)
        else:
            i=i+1
    data1['buyers'].append(data)
    with open('dbfiles/buyers.json', "w") as f:
        json.dump(data1, f, indent=4)

def update_cart(data):
    data1=read('carts.json')
    i=0
    for c in data1['carts']:
        if c['buyer_email']==data['buyer_email']:
            data1['carts'].pop(i)
        else:
            i=i+1
    data1['carts'].append(data)
    with open('dbfiles/carts.json', "w") as f:
        json.dump(data1, f, indent=4)

def update_order(data):
    data1=read('orders.json')
    i=0
    for o in data1['orders']:
        if o['order_id']==data['order_id']:
            data1['orders'].pop(i)
        else:
            i=i+1
    data1['orders'].append(data)
    with open('dbfiles/orders.json', "w") as f:
        json.dump(data1, f, indent=4)

def update_order_history(data):
    data1=read('orderhistory.json')
    i=0
    for o in data1['order_history']:
        if o['buyer_email']==data['buyer_email']:
            data1['order_history'].pop(i)
        else:
            i=i+1
    data1['order_history'].append(data)
    with open('dbfiles/orderhistory.json', "w") as f:
        json.dump(data1, f, indent=4)

def delete_product(data):
    data1=read('products.json')
    i=0
    for p in data1['products']:
        if p['product_id']==data['product_id']:
            data1['products'].pop(i)
        else:
            i=i+1
    with open('dbfiles/products.json',"w") as f:
        json.dump(data1, f, indent=4)

