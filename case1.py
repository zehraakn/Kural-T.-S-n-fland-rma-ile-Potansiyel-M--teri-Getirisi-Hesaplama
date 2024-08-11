import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#Soru 1:
# Veri setini yükle
df = pd.read_excel('miuul_gezinomi.xlsx')

# Veri seti hakkında temel bilgileri göster
print(df.head())
print(df.shape)
print(df.info())

# Soru 2: Kaç tane unique şehir var? Frekansları nedir?
unique_cities = df["SaleCityName"].nunique()
city_frequencies = df["SaleCityName"].value_counts()
print(f"Unique şehir sayısı: {unique_cities}")
print(city_frequencies)

# Soru 3: Kaç tane unique Concept var?
unique_concepts = df["ConceptName"].nunique()
print(f"Unique Concept sayısı: {unique_concepts}")

# Soru 4: Hangi Concept'ten kaçar tane satış gerçekleşmiş?
concept_sales = df["ConceptName"].value_counts()
print(concept_sales)

# Soru 5: Şehirlere göre toplam kazanç nedir?
city_earnings = df.groupby("SaleCityName").agg({"Price": "sum"})
print(city_earnings)

# Soru 6: Concept türlerine göre toplam kazanç nedir?
concept_earnings = df.groupby("ConceptName").agg({"Price": "sum"})
print(concept_earnings)

# Soru 7: Şehirlere göre PRICE ortalamaları nedir?
city_avg_price = df.groupby(by=['SaleCityName']).agg({"Price": "mean"})
print(city_avg_price)

# Soru 8: Concept'lere göre PRICE ortalamaları nedir?
concept_avg_price = df.groupby(by=['ConceptName']).agg({"Price": "mean"})
print(concept_avg_price)

# Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
city_concept_avg_price = df.groupby(by=["SaleCityName", 'ConceptName']).agg({"Price": "mean"})
print(city_concept_avg_price)

# Görev 2: satis_checkin_day_diff değişkenini EB_Score adında yeni bir kategorik değişkene çevir
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Son Dakikacılar", "Potansiyel Planlayıcılar", "Planlayıcılar", "Erken Rezervasyon Yapanlar"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)

# Görev 3: Şehir, Concept, [EB_Score, Sezon, CInDay] kırılımında ücret ortalamalarına ve frekanslarına bak
# Şehir-Concept-EB Score kırılımında ücret ortalamaları
city_concept_ebscore_avg_price = df.groupby(by=["SaleCityName", 'ConceptName', "EB_Score"]).agg({"Price": ["mean", "count"]})
print(city_concept_ebscore_avg_price)

# Şehir-Concept-Sezon kırılımında ücret ortalamaları
city_concept_season_avg_price = df.groupby(by=["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})
print(city_concept_season_avg_price)

# Şehir-Concept-CInDay kırılımında ücret ortalamaları
city_concept_cinday_avg_price = df.groupby(by=["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})
print(city_concept_cinday_avg_price)

# Görev 4: Şehir-Concept-Sezon kırılımını PRICE'a göre sırala
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
print(agg_df.head(20))

# Görev 5: Indekste yer alan isimleri değişken ismine çevir
agg_df.reset_index(inplace=True)
print(agg_df.head())

# Görev 6: Yeni seviye tabanlı satışları tanımla ve veri setine değişken olarak ekle
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)
print(agg_df.head())

# Görev 7: Personaları segmentlere ayır
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
print(agg_df.head(30))
print(agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]}))

# Görev 8: Son df'i PRICE değişkenine göre sırala
agg_df = agg_df.sort_values(by="Price", ascending=False)
print(agg_df.head())

# "ANTALYA_HERŞEY DAHIL_HIGH" hangi segmentte ve ne kadar ücret bekleniyor?
new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
new_user_info = agg_df[agg_df["sales_level_based"] == new_user]
print(new_user_info)

