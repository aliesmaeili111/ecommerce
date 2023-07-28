# from home.models import Product

# Compare_SESSION_ID = 'compare'
        
# class NewCompare:
#     def __init__(self, request):
#         self.session = request.session
#         compare = self.session.get(Compare_SESSION_ID)
#         if not compare:
#             compare = self.session[Compare_SESSION_ID] = {}
#         self.compare = compare

#     def remove(self, product):
#         product_id = str(product.id)
#         if product_id in self.compare:
#             del self.compare[product_id]
#             self.save()

#     def add(self, product):
#         product_id = str(product.id)
#         if product_id not in self.compare:
#             self.compare[product_id]['product'] = {'id': product_id}
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def __iter__(self):
#         products_ids = self.compare.keys()
#         products = Product.objects.filter(id__in=products_ids)
#         compare = self.compare.copy()
#         for product in products:
#             compare[str(product.id)]['product'] = product

#         for data in self.compare.values():
#             yield data
