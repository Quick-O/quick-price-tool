import streamlit as st

# 仮データ定義
customers = {
    "クイック": {"カテゴリ1": 0.85, "カテゴリ2": 0.90, "カテゴリ3": 1.0},
    "平田": {"カテゴリ1": 0.80, "カテゴリ2": 0.88, "カテゴリ3": 0.95}
}

products = {
    "ポスター": {
        "マット紙": {
            "つやなし": "CT001",
            "光沢紙": "CT002"
        },
        "コート紙": {
            "つやあり": "CT003"
        }
    }
}

standard_prices = {
    "CT001": 1000,
    "CT002": 1200,
    "CT003": 1100
}

rounding = {
    "カテゴリ1": 10,
    "カテゴリ2": 100,
    "カテゴリ3": 1
}

options = {
    "PP加工": 300,
    "ラミネート": 500
}

size_master = {
    "A4": 0.062,
    "B4": 0.088,
    "A3": 0.124
}

st.title("クイック価格検索ツール")

customer = st.selectbox("顧客を選択してください", list(customers.keys()))
st.write("掛率：", customers[customer])

cat1 = st.selectbox("カテゴリ1（区分1）を選択", list(products.keys()))
cat2 = st.selectbox("カテゴリ2（区分2）を選択", list(products[cat1].keys()))
cat3 = st.selectbox("カテゴリ3（区分3）を選択", list(products[cat1][cat2].keys()))

ct_code = products[cat1][cat2][cat3]
st.write(f"選択された商品コード（Ct）: {ct_code}")

col1, col2 = st.columns(2)
width = col1.number_input("短辺（mm）", min_value=1, value=210)
length = col2.number_input("長辺（mm）", min_value=1, value=297)

area = (width / 1000) * (length / 1000)
st.write(f"入力サイズの面積：{area:.3f} ㎡")

base_size = None
for name, size_area in sorted(size_master.items(), key=lambda x: x[1]):
    if size_area >= area:
        base_size = name
        base_area = size_area
        break

if base_size:
    st.write(f"基準サイズ：{base_size}（{base_area}㎡）")
    area_ratio = area / base_area
else:
    st.error("該当する基準サイズが見つかりません。")
    area_ratio = 1.0

price_parts = []
for cat in ["カテゴリ1", "カテゴリ2", "カテゴリ3"]:
    rate = customers[customer][cat]
    std_price = standard_prices.get(ct_code, 0)
    r = rounding[cat]
    partial_price = round(std_price * rate * area_ratio / r) * r
    price_parts.append((cat, partial_price))

selected_options = st.multiselect("オプションを選択", list(options.keys()))
option_total = sum(options[opt] for opt in selected_options)

total_price = sum(p[1] for p in price_parts) + option_total

st.subheader("価格内訳")
for cat, val in price_parts:
    st.write(f"{cat}: ¥{val:,}")
st.write(f"オプション合計: ¥{option_total:,}")

st.subheader(f"■ 合計金額：¥{total_price:,}（税込）")
