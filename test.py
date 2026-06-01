import joblib
import os

print("--- DIRECTORY CHECK ---")
print("Current Directory Files:", os.listdir('.'))

print("\n--- PICKLE LOADING MATRIX ---")
try:
    cols = joblib.load("heart_columns.pkl")
    print("✅ success: 'heart_columns.pkl' loaded perfectly.")
    print("📌 Model expects these exact columns:\n", cols)
except Exception as e:
    print("❌ fail: Could not load columns. Error:", e)