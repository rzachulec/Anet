puste_kolumny = wszystkie.iloc[4:].isna().all()
# wszystkie.drop(wszystkie.columns[puste_kolumny], axis=1, inplace=True)