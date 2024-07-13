import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('investments_VC.csv')

'''очищення данних'''

df = df.drop(["permalink", "name", "homepage_url", "region", "city", "state_code", "country_code", "status", "founded_quarter"], axis=1)

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

#найпопулярніші категорії
most_popular_category = high_funding['category_list'].value_counts().idxmax()
most_popular_category_count = high_funding['category_list'].value_counts().max()

# Виведення найпопулярнішого ринку
most_popular_market = high_funding['market'].value_counts().idxmax()
most_popular_market_count = high_funding['market'].value_counts().max()

#чи впливає початковий етап фінансування компанії (seed) на успішність
if df[df['seed'] > 0]['funding_rounds'].mean() > df[df['seed'] <= 0]['funding_rounds'].mean():
    print('seed впливає')
else:
    print('seed не впливає')

print(f"Найпопулярніший ринок: {most_popular_market}")
print(f"К-сть успішних стартапів на цьому ринку: {most_popular_market_count}")

print(f"Найпопулярніша категорія: {most_popular_category}")
print(f"К-сть успішних стартапів з цею категорією: {most_popular_category_count}")

# df[df['funding_total_usd'] >= 100000]['market'].value_counts().nlargest(10).plot(kind='barh')
# df[df['funding_total_usd'] >= 100000]['category_list'].value_counts().nlargest(10).plot(kind='barh')
d3 = df[df['seed'] > 0]['funding_rounds'].nlargest(1)
d4 = df[df['seed'] <= 0]['funding_rounds'].nlargest(1)
d3.plot(kind='barh', )
d4.plot(kind='barh')

plt.show()
df.info()
df.to_csv("clear_csv.csv")