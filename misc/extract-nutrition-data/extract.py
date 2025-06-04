import pandas as pd

wybrane_kody = pd.read_excel('extract-nutrition-data/Lista receptur i surowcow.xls')
wszystkie = pd.read_csv('extract-nutrition-data/Surowce PetFood.csv', encoding='latin2', delimiter=';', low_memory=False)

# wszystkie.dropna(axis=1, how='all', inplace=True)
# wszystkie.dropna(axis=0, how='all', inplace=True)

# # wybrane_kody = wybrane_kody.iloc[1:]

# wybrane_kody.dropna(axis=1, how='all', inplace=True)
# wybrane_kody.dropna(axis=0, how='all', inplace=True)


# puste_kolumny = wszystkie.iloc[4:].isna().all()
# wszystkie.drop(wszystkie.columns[puste_kolumny], axis=1, inplace=True)

print(wybrane_kody.head())
print(wszystkie.head())

lista_kodow = wybrane_kody['Surowce'].values.tolist()
lista_kodow = [str(kod) for kod in lista_kodow]

# filtered_kodow = set(lista_kodow)
lista_kodow.append('Desc')
# & set(wszystkie['Ing_Code'])
# print(filtered_kodow)
print(lista_kodow)
# print(len(filtered_kodow))
print(len(lista_kodow))
print(wszystkie.shape)

wszystkie = wszystkie[wszystkie['Ing_Code'].isin(lista_kodow)]

wszystkie.to_csv('extract-nutrition-data/filtered.csv', index=False)



