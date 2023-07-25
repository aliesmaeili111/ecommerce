from home.models import Product

COMPARE_SESSIOAN_ID = 'compare'
class Compare:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(COMPARE_SESSIOAN_ID)
        if not compare:
            compare = self.session[COMPARE_SESSIOAN_ID] = {}
        self.compare = compare
            
    def add(self,product):
        product_id = str(product.id)
        if product_id not in self.compare:
            self.compare[product_id] = {'id':product_id}
        self.save()
        
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.compare:
            del self.compare[product_id]
        self.save()
        
    def save(self):
        self.session.modified = True
        
    def __iter__(self):
        prodcuts_ids = self.compare.keys()
        products = Product.objects.filter(id__in=prodcuts_ids)
        
        for product in products:
            self.compare[str(product.id)]['product'] = product
            
        for data in self.compare.values():
            yield data