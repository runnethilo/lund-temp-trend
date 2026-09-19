import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

df = pd.read_csv("smhi-opendata_1_53430_20260919_091243.csv", sep=";")

df = df.drop(columns=["Tid (UTC)", "Tidsutsnitt:"])
df = df[df["Kvalitet"] == "G"] 
df = df.drop(columns = "Kvalitet")


df["Datum"] = df["Datum"].str[:7] #gör om så vi bara har varje månad istället för exakt datum

measurement_count = df.groupby("Datum").count() #kolla hur många mätningar det finns per månad

measurement_count = measurement_count[measurement_count["Lufttemperatur"] >= 50] #tar bort månader med mindre än 50 mätningar

measurement_count.index = measurement_count.index.str[:4] #gör om allt så vi har det per år

measurement_count = measurement_count.groupby(level=0).count() #kollar hur många månader det finns mätningar för per år

measurement_count = measurement_count[measurement_count["Lufttemperatur"] == 12] #tar bort allt som inte har 12 månader av mätningar

complete_years = measurement_count.index.to_list() #gör om alla år som är kvar till en lista

df["Datum"] = df["Datum"].str[:4]

df = df[df["Datum"].isin(complete_years)]



df["Datum"] = df["Datum"].astype(int) #gör om det till en integer från en strän igen

df = df.groupby("Datum").mean() #gruppera per datum och kolla medelvärdet för temperaturen

year = df.index #index tar året som index
temp = df["Lufttemperatur"].tolist() #gör om Lufttemperaturen till en lista som vi kan använda som y

x = year
y = temp

k, m = np.polyfit(x, y, 1)

plt.scatter(x, y, label="Measurement data")
plt.plot(x, k*x + m, "r", label=f"Linear regression, 10k = {10 * round(k, 5)} °C/10 år")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Average temp, °C")
plt.title("Average temperature over time in Lund")
plt.show()