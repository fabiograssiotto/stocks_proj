# Código de teste para avaliar a biblioteca newsapi.
from newsapi.sources import Sources
from newsapi.articles import Articles
s = Sources(API_KEY = "f1ed47573d904a988baf98f093f11086")
a = Articles(API_KEY = "f1ed47573d904a988baf98f093f11086")

res = (a.get(source='wired-de'))
print(res.articles[0]['title'])