
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# CSV 데이터 불러오기
df = pd.read_csv("data/owid-co2-data.csv")

# 세계 데이터만 추출
world = df[df["country"] == "World"].sort_values("year")
world = world.dropna(subset=["co2"])

# 최신 연도 및 전년도 데이터
latest = world.iloc[-1]
previous = world[world["year"] == latest["year"] - 1]

latest_year = int(latest["year"])

# 1. 세계 CO2 배출량 (Mt -> Gt)
world_co2 = latest["co2"] / 1000

# 2. 세계 1인당 CO2 배출량
world_per_capita = latest["co2_per_capita"]

# 3. 전년 대비 CO2 배출 증가율
if not previous.empty:
    previous_co2 = previous.iloc[-1]["co2"]
    growth_rate = (latest["co2"] - previous_co2) / previous_co2 * 100
else:
    growth_rate = None

# 4. 세계 누적 CO2 배출량 (Mt -> Tt)
if "cumulative_co2" in world.columns:
    cumulative_co2 = latest["cumulative_co2"] / 1_000_000
else:
    cumulative_co2 = None


@app.route("/")
def home():
    return render_template(
        "index.html",
        latest_year=latest_year,
        world_co2=world_co2,
        world_per_capita=world_per_capita,
        growth_rate=growth_rate,
        cumulative_co2=cumulative_co2
    )


if __name__ == "__main__":
    app.run(debug=True)
