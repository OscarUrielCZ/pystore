import click
from os import path
from article import commands as article_commands

TABLE_NAME = path.join(path.dirname(path.abspath(__file__)), '.articles.csv')

@click.group()
@click.pass_context
def cli(ctx):
	"""A manage store app"""
	ctx.obj = {}
	ctx.obj['table_name'] = TABLE_NAME

cli.add_command(article_commands.all)