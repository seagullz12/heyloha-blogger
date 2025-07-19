from ai_agents.blog_agent import write_blog_func, Article

articles = [
    Article(title="Voorbeeld Nieuws", description="Dit is een test van de bloggenerator."),
]

result = write_blog_func(articles)
print(result)
