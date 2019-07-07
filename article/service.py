import csv

from article.model import Article

class ArticleService:
	def __init__(self, table_name):
		self._table_name = table_name

	def create_article(self, article):
		articles = [Article(**article) for article in self.articles_list()]
		if article in articles:
			return False
		with open(self._table_name, 'a') as f:
			writer = csv.DictWriter(f, fieldnames=Article.schema())
			writer.writerow(article.to_dict())
			return True

	def get_article(self, article_uid):
		for article in self.articles_list():
			if article['uid'] == article_uid:
				return Article(**article)
		return None

	def articles_list(self):
		with open(self._table_name, 'r') as f:
			reader = csv.DictReader(f, fieldnames=Article.schema())
			return list(reader)

	def update_article(self, new_article):
		updated_articles = []
		for article in self.articles_list():
			if article['uid'] == new_article.uid:
				updated_articles.append(new_article.to_dict())
			else:
				updated_articles.append(article)
		self._save_to_disk(updated_articles)
		return True

	def delete_article(self, article_uid):
		articles = self.articles_list()
		article_deleted_list = list(filter(lambda article: article['uid'] != article_uid, articles))
		if len(articles) == len(article_deleted_list):
			return False
		self._save_to_disk(article_deleted_list)
		return True

	def _save_to_disk(self, articles_list):
		with open(self._table_name, 'w') as f:
			writer = csv.DictWriter(f, fieldnames=Article.schema())
			writer.writerows(articles_list)