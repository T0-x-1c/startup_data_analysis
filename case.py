import pandas as pd

df = pd.read_csv('investments_VC.csv')

'''очищення данних'''

df = df.drop("permalink", axis=1)
df = df.drop("name", axis=1)
df = df.drop("homepage_url", axis=1)
df = df.drop("region", axis=1)
df = df.drop("city", axis=1)
df = df.drop("state_code", axis=1)
df = df.drop("country_code", axis=1)
df = df.drop("status", axis=1)
df = df.drop("founded_quarter", axis=1)

def category_list_normalization(category_list):
    category_list = str(category_list)
    return category_list[1:-2].replace("|", ",")

def funding_total_usd_normalization(funding_total_usd):
    if funding_total_usd != ' -   ':
        return int(funding_total_usd.replace(",", ""))
    else:
        return 0

df.columns = df.columns.str.strip()

df = df.dropna(subset=['market', 'category_list'])

df["category_list"] = df["category_list"].apply(category_list_normalization)
df["funding_total_usd"] = df["funding_total_usd"].apply(funding_total_usd_normalization)

'''доведення гіпотези'''
#стартапи в які інвестували 100к і ні
high_funding = df[df['funding_total_usd'] >= 100000]
low_funding = df[df['funding_total_usd'] < 100000]

#к-сть раундів фінансування в цих стартапах
# перевіряємо чи вірна гіпотиза
if high_funding['funding_rounds'].mean() > low_funding['funding_rounds'].mean():
    print('гіпотеза доведена')
else:
    print('гіпотеза спрощана')

# print(high_funding['funding_rounds'].mean(), low_funding['funding_rounds'].mean())

'''які чинники впливають на успіх стартапу'''

df.info()
df.to_csv("clear_csv.csv")