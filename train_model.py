import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load Dataset
print("📂 Loading dataset...")
df = pd.read_csv('dataset.csv')
print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Feature Selection
feature_columns = [
    'Relative Compactness',
    'Surface Area',
    'Wall Area',
    'Roof Area',
    'Overall Height',
    'Orientation',
    'Glazing Area',
    'Glazing Distribution'
]

target_columns = ['Heating Load', 'Cooling Load']

X = df[feature_columns]
y_heating = df['Heating Load']
y_cooling = df['Cooling Load']

print(f"\n📊 Features: {list(X.columns)}")
print(f"🎯 Targets: Heating Load, Cooling Load")

# Train-Test Split
X_train, X_test, y_heating_train, y_heating_test = train_test_split(
    X, y_heating, test_size=0.2, random_state=42
)

_, _, y_cooling_train, y_cooling_test = train_test_split(
    X, y_cooling, test_size=0.2, random_state=42
)

print(f"\n📈 Training set size: {X_train.shape[0]} samples")
print(f"📉 Testing set size: {X_test.shape[0]} samples")

# Train Random Forest Model for Heating Load
print("\n🔥 Training Heating Load Model...")
heating_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
heating_model.fit(X_train, y_heating_train)

# Train Random Forest Model for Cooling Load
print("❄️ Training Cooling Load Model...")
cooling_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
cooling_model.fit(X_train, y_cooling_train)

# Make Predictions
y_heating_pred = heating_model.predict(X_test)
y_cooling_pred = cooling_model.predict(X_test)

# Evaluate Heating Load Model
print("\n" + "="*50)
print("HEATING LOAD MODEL EVALUATION")
print("="*50)
print(f"R² Score: {r2_score(y_heating_test, y_heating_pred):.4f}")
print(f"Mean Absolute Error: {mean_absolute_error(y_heating_test, y_heating_pred):.4f}")
print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_heating_test, y_heating_pred)):.4f}")

# Evaluate Cooling Load Model
print("\n" + "="*50)
print("COOLING LOAD MODEL EVALUATION")
print("="*50)
print(f"R² Score: {r2_score(y_cooling_test, y_cooling_pred):.4f}")
print(f"Mean Absolute Error: {mean_absolute_error(y_cooling_test, y_cooling_pred):.4f}")
print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_cooling_test, y_cooling_pred)):.4f}")

# Cross-Validation
print("\n" + "="*50)
print("CROSS-VALIDATION RESULTS")
print("="*50)

heating_cv_scores = cross_val_score(heating_model, X, y_heating, cv=5, scoring='r2')
cooling_cv_scores = cross_val_score(cooling_model, X, y_cooling, cv=5, scoring='r2')

print(f"Heating Model CV R²: {heating_cv_scores.mean():.4f} (+/- {heating_cv_scores.std()*2:.4f})")
print(f"Cooling Model CV R²: {cooling_cv_scores.mean():.4f} (+/- {cooling_cv_scores.std()*2:.4f})")

# Feature Importance
print("\n" + "="*50)
print("FEATURE IMPORTANCE ANALYSIS")
print("="*50)

heating_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': heating_model.feature_importances_
}).sort_values('importance', ascending=False)

cooling_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': cooling_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🔥 Heating Load - Top Features:")
for i, row in heating_importance.head(5).iterrows():
    print(f"   • {row['feature']}: {row['importance']:.3f}")

print("\n❄️ Cooling Load - Top Features:")
for i, row in cooling_importance.head(5).iterrows():
    print(f"   • {row['feature']}: {row['importance']:.3f}")

# Save Models
print("\n💾 Saving models...")

# Save as dictionary for combined model
model_package = {
    'heating_model': heating_model,
    'cooling_model': cooling_model,
    'feature_columns': feature_columns,
    'heating_importance': heating_importance,
    'cooling_importance': cooling_importance
}

with open('model.pkl', 'wb') as file:
    pickle.dump(model_package, file)

print("✅ Model saved as 'model.pkl'")

# Sample Prediction
print("\n" + "="*50)
print("SAMPLE PREDICTION")
print("="*50)

sample = np.array([[0.76, 670.5, 295.5, 110.0, 3.5, 3, 0.10, 4]])
heating_pred = heating_model.predict(sample)[0]
cooling_pred = cooling_model.predict(sample)[0]

print(f"Sample Input: Compactness=0.76, Surface=670.5, Wall=295.5, Roof=110.0, Height=3.5, Orientation=3, Glazing=0.10, Distribution=4")
print(f"🔥 Predicted Heating Load: {heating_pred:.2f} kWh/m²")
print(f"❄️ Predicted Cooling Load: {cooling_pred:.2f} kWh/m²")

print("\n🎉 Training complete! You can now run the Streamlit app.")