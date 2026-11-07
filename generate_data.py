import random
import sqlite3
import os
from datetime import timedelta
from faker import Faker

os.makedirs("data", exist_ok = True)

random.seed(42)
Faker.seed(42)
fake = Faker()

conn = sqlite3.connect("data/inventory.db")
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS codes;
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    platform TEXT NOT NULL,
    edition TEXT NOT NULL,
    price_usd REAL NOT NULL,
    reorder_threshold INTEGER NOT NULL
);
CREATE TABLE codes (
    code TEXT PRIMARY KEY,
    sku TEXT NOT NULL REFERENCES products(sku),
    status TEXT NOT NULL CHECK (status IN ('available', 'redeemed', 'revoked')),
    retailer TEXT NOT NULL,
    created_at TEXT NOT NULL,
    redeemed_at TEXT,
    revoked_reason TEXT
);
""")

# 7 invented game titles and the 3 platforms they are on.
TITLES = [
    "Animal Thieves",
    "Captain Invincible",
    "Tommy And The Hidden Forest",
    "Network Dream 4",
    "Elemental Chaos 2",
    "When Leaves Fall",
    "Gabriel And The Seven Kingdoms",
]

PLATFORMS = ["PlayStation", "Xbox", "Nintendo"]
# Builds 21 product rows from TITLES and PLATFORMS, keeps the first 20.
# The edition and threshold are random; the price and SKU code follow from the edition.
# The threshold is the reorder point: the number of available codes below which a product counts as low stock.
products = []
EDITION_CODES = {"Standard": "STD", "Deluxe": "DLX"}
PRICES = {"Standard": 59.99, "Deluxe": 69.99}
for title in TITLES:
    for platform in PLATFORMS:
        edition = random.choice(["Standard", "Deluxe"])
        sku = f"{title.split()[0].upper()}-{platform[:2].upper()}-{EDITION_CODES[edition]}"
        price = PRICES[edition]
        threshold = random.randint(40, 80)
        products.append((sku, title, platform, edition, price, threshold))
products = products[:20]

print(len(products), products[:3])
# TODO 3: make 5,000 code rows. For each: pick a SKU (unevenly), make a unique
#         code string, pick a status with random.choices(..., weights=[...]),
#         and fill redeemed_at / revoked_reason only when they apply.
# TODO 4: insert both lists with cur.executemany(...), then conn.commit().