import uuid

class Article:
	"""Is a product class"""

	def __init__(self, name, brand, price, content, uid=None):
		self.uid = uid or uuid.uuid4()
		self.name = name
		self.brand = brand
		self.price = price
		self.content = content

	def __eq__(self, article):
		return self.uid == article.uid or (self.name == article.name and self.brand == article.brand and self.content == article.content)

	def __str__(self):
		return f'{self.name} {self.brand} {self.content}'

	def to_dict(self):
		return vars(self)

	@staticmethod
	def schema():
		return ['uid', 'name', 'brand', 'price', 'content']