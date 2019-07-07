import click

from article.model import Article
from article.service import ArticleService

@click.group()
def article():
	"""Provides article services"""
	pass

@article.command()
@click.option('-u', '--article_uid',
				type=str,
				prompt=True,
				help='The article uid you want to buy')
@click.option('-q', '--quantity',
				type=int,
				prompt=True,
				help='How many articles')
@click.pass_context
def buy(ctx, article_uid, quantity):
	"""Buy an article"""
	pass

@article.command()
@click.option('-n', '--name',
				type=str,
				prompt=True,
				help='The new article name')
@click.option('-b', '--brand',
				type=str,
				prompt=True,
				help='The new article brand')
@click.option('-p', '--price',
				type=int,
				prompt=True,
				help='The new article price')
@click.option('-c', '--content',
				type=str,
				prompt=True,
				help='The new article content')
@click.pass_context
def create(ctx, name, brand, price, content):
	"""Create a new article"""
	article = Article(name, brand, price, content)
	article_service = ArticleService(ctx.obj['table_name'])
	status = article_service.create_article(article)
	if status:
		click.echo(f'Successful register of {article}')
	else:
		click.echo(f'Error: the article {article} already exists')

@article.command()
@click.pass_context
def list(ctx):
	"""List all the articles"""
	article_service = ArticleService(ctx.obj['table_name'])
	articles = article_service.articles_list()

	click.echo('               uid                |   name   |   brand   |  price  | content ')
	click.echo('*' * 80)
	for article in articles:
		click.echo(f"{article['uid']} | {article['name']} | {article['brand']} | {article['price']} | {article['content']}")

@article.command()
@click.option('-u', '--uid',
				type=str,
				prompt=True,
				help='The article uid you want to update')
@click.pass_context
def update(ctx, uid):
	"""Update an article"""
	article_service = ArticleService(ctx.obj['table_name'])
	article = article_service.get_article(uid)

	if article:
		article = _update_article_flow(article)
		status = article_service.update_article(article)

		if status:
			click.echo('Successful article update')
		else:
			click.echo('Error: something went wrong')
	else:
		click.echo(f'Error: the article with uid {uid} doesnt exists')

@article.command()
@click.option('-u', '--uid',
				type=str,
				prompt=True,
				help='The article uid you want to delete')
@click.pass_context
def delete(ctx, uid):
	"""Delete an article"""
	article_service = ArticleService(ctx.obj['table_name'])
	status = article_service.delete_article(uid)

	if status:
		click.echo('Successful article delete')
	else:
		click.echo(f'Error: the article with uid {uid} doesnt exists')

def _update_article_flow(article):
	click.echo('Leave empty for no changes')

	article.name = click.prompt('New name', type=str, default=article.name)
	article.brand = click.prompt('New brand', type=str, default=article.brand)
	article.price = click.prompt('New price', type=str, default=article.price)
	article.content = click.prompt('New content', type=str, default=article.content)

	return article	

all = article