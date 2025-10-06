from .models import Product
class CompareProduct:
    def __init__(self, request):
        self.session = request.session
        compare_product=self.session.get('compare_product')
        if not compare_product:
            compare_product=self.session['compare_product']=[]
        self.compare_product=compare_product
        self.count=len(self.compare_product)
        #-----------------------------------------------------------
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item
        #-----------------------------------------------------------
    def add_to_compare_product(self,product_id,product_group_id):
        product_id=int(product_id)
        temp=self.compare_product
        if temp:
            product1=Product.objects.get(id=temp[0])
            product2=Product.objects.get(id=product_id)
            if product1.getMainProductGroups() == product2.getMainProductGroups():
                if product_id not in self.compare_product:
                    self.compare_product.append(product_id)
                    self.count=len(self.compare_product)
                    self.session.modified=True
                else:
                    return True
            else:
                return False
        else:
            if product_id not in self.compare_product:
                self.compare_product.append(product_id)
                self.count=len(self.compare_product)
                self.session.modified=True
            
        #-----------------------------------------------------------
    def delete_from_compare_product(self, product_id):
        product_id = int(product_id)
        if product_id in self.compare_product:
            self.compare_product.remove(product_id)
        self.count = len(self.compare_product)
        self.session.modified = True
        #-----------------------------------------------------------