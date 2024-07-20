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

def main_category(category_list):
    category_list = category_list.split(",")[0]
    return category_list

df.columns = df.columns.str.strip()

df = df.dropna(subset=['market', 'category_list'])

df["category_list"] = df["category_list"].apply(category_list_normalization)
df["funding_total_usd"] = df["funding_total_usd"].apply(funding_total_usd_normalization)
df['main_category'] = df['category_list'].apply(main_category)

'''доведення гіпотези'''
#стартапи в які інвестували 100к і ні
high_funding = df[df['funding_total_usd'] >= 100000]
low_funding = df[df['funding_total_usd'] < 100000]

#к-сть раундів фінансування в цих стартапах
# перевіряємо чи вірна (гіпотиза 1)
if high_funding['funding_rounds'].mean() > low_funding['funding_rounds'].mean():
    print('гіпотеза доведена')
else:
    print('гіпотеза спрощана')



# print(high_funding['funding_rounds'].mean(), low_funding['funding_rounds'].mean())

'''які чинники впливають на успіх стартапу'''

#найпопулярніші категорії
most_popular_category = high_funding['main_category'].value_counts().idxmax()
most_popular_category_count = high_funding['main_category'].value_counts().max()

# Виведення найпопулярнішого ринку
most_popular_market = high_funding['market'].value_counts().idxmax()
most_popular_market_count = high_funding['market'].value_counts().max()

#чи впливає початковий етап фінансування компанії (seed) на успішність (гіпотиза 2)
if df[df['seed'] > 0]['funding_rounds'].mean() > df[df['seed'] <= 0]['funding_rounds'].mean():
    print('seed впливає')
else:
    print('seed не впливає')

print(f"Найпопулярніший ринок: {most_popular_market}")
print(f"К-сть успішних стартапів на цьому ринку: {most_popular_market_count}")

print(f"Найпопулярніша категорія: {most_popular_category}")
print(f"К-сть успішних стартапів з цею категорією: {most_popular_category_count}")

#гіпотиза 3, стартапи в певних категоріях отримують більше фінансування порівняно з іншими категоріями
category_funding = df.groupby('main_category')['funding_total_usd'].sum()
category_funding.nlargest(10).plot(kind="pie")

most_funded_category = category_funding.idxmax()

print(f"Категорія з найбільшим фінансуванням: {most_funded_category}")

# df[df['funding_total_usd'] >= 100000]['market'].value_counts().nlargest(10).plot(kind='barh')
# df[df['funding_total_usd'] >= 100000]['category_list'].value_counts().nlargest(10).plot(kind='barh')

# d3 = df[df['seed'] > 0]['funding_rounds'].nlargest(1000)
# d4 = df[df['seed'] <= 0]['funding_rounds'].nlargest(1000)

# # Побудова графіку
# fig, ax = plt.subplots()

# # додавання d3
# ax.barh(d3.index, d3.values, color='blue', label='Seed > 0')

# # додавання d4
# ax.barh(d4.index, d4.values, color='green', label='Seed <= 0')

# # додавання написів і легенди на графік
# ax.set_xlabel('Number of Funding Rounds')
# ax.set_title('Comparison of Funding Rounds')
# ax.legend()



plt.show()

df.info()
df.to_csv("clear_csv.csv")