import intrinio

intrinio.client.username = 'cbf3647ca29bd2236958b388b875b9fd'
intrinio.client.password = '932441d13c084642d3bfece69acb1227'

df_appl = intrinio.news('AAPL')
df_appl.to_csv('AAPL.csv')
df_googl = intrinio.news('GOOGL')
df_googl.to_csv('GOOGL.csv')
df_msft = intrinio.news('MSFT')
df_msft.to_csv('MSFT.csv')
df_fb = intrinio.news('FB')
df_fb.to_csv('FB.csv')
df_tsm = intrinio.news('TSM')
df_tsm.to_csv('TSM.csv')
