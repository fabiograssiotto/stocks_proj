# Script para extrair dados de notícias do site intrinio
# das 10 ações de tecnologia com maor Market Cap negociadas na NASDAQ.
import intrinio

# O site intrinio fornece acesso à API através de username e senha
# a API tem limites de utilização diária, por isso duas contas foram utilizadas
# para executar o fetch.
#intrinio.client.username = 'cbf3647ca29bd2236958b388b875b9fd'
#intrinio.client.password = '932441d13c084642d3bfece69acb1227'

intrinio.client.username = '9ef28500250f001837e864630f98010d'
intrinio.client.password = 'b6d38989841c00d252232a7ef1822f20'

# Extrai notícias em dataframe pandas e grava em CSV.
df_appl = intrinio.news('AAPL')
df_appl.to_csv('news/AAPL.csv')
df_googl = intrinio.news('GOOGL')
df_googl.to_csv('news/GOOGL.csv')
df_msft = intrinio.news('MSFT')
df_msft.to_csv('news/MSFT.csv')
df_fb = intrinio.news('FB')
df_fb.to_csv('news/FB.csv')
df_tsm = intrinio.news('TSM')
df_tsm.to_csv('news/TSM.csv')
df_csco = intrinio.news('CSCO')
df_csco.to_csv('news/CSCO.csv')
df_intc = intrinio.news('INTC')
df_intc.to_csv('news/INTC.csv')
df_orcl = intrinio.news('ORCL')
df_orcl.to_csv('news/ORCL.csv')
df_ibm = intrinio.news('IBM')
df_ibm.to_csv('news/IBM.csv')
df_sap = intrinio.news('SAP')
df_sap.to_csv('news/SAP.csv')
