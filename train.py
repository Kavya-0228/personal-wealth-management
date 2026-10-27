import os
import json
import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

def main():
    print("=" * 60)
    print("STEP 1 — LOAD DATA")
    print("=" * 60)
    
    csv_path = "personal_wealth_management_dataset.csv"
    df = pd.read_csv(csv_path)
    
    print(f"Dataset Shape: {df.shape}")
    print("\nColumn Names:")
    print(df.columns.tolist())
    
    print("\nData Types:")
    print(df.dtypes)
    
    print("\nFirst 5 Rows:")
    print(df.head())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate Rows: {duplicate_count}")
    
    print("\nStatistical Summary:")
    print(df.describe())
    
    print("\n" + "=" * 60)
    print("STEP 2 — CLEAN DATA")
    print("=" * 60)
    
    # Check for duplicate records and drop if needed, but do not delete rows unnecessarily
    if duplicate_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Removed {duplicate_count} duplicate rows. New shape: {df.shape}")
    else:
        print("No duplicate records found.")
        
    print("Missing numerical values will be handled using median imputation during pipeline processing.")
    
    print("\n" + "=" * 60)
    print("STEP 3 — SELECT FEATURES & TARGET")
    print("=" * 60)
    
    feature_cols = [
        'age',
        'monthly_income',
        'monthly_expense',
        'monthly_savings',
        'current_savings',
        'debt',
        'financial_goal_amount',
        'investment_horizon_years',
        'risk_tolerance_score'
    ]
    target_col = 'risk_category'
    
    print(f"Selected Features ({len(feature_cols)}): {feature_cols}")
    print(f"Target Column: {target_col}")
    
    X = df[feature_cols]
    y = df[target_col]
    
    print(f"\nTarget Class Distribution:")
    print(y.value_counts())
    
    print("\n" + "=" * 60)
    print("STEP 4 — TRAIN TEST SPLIT")
    print("=" * 60)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples: {X_test.shape[0]}")
    
    print("\n" + "=" * 60)
    print("STEP 5 & 6 — TRAIN AND EVALUATE MODELS")
    print("=" * 60)
    
    pipelines = {
        'Logistic Regression': Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('classifier', LogisticRegression(random_state=42, max_iter=1000))
        ]),
        'Decision Tree Classifier': Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('classifier', DecisionTreeClassifier(random_state=42))
        ]),
        'Random Forest Classifier': Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('classifier', RandomForestClassifier(random_state=42))
        ])
    }
    
    results = {}
    reports = {}
    confusion_matrices = {}
    trained_pipelines = {}
    
    for name, pipeline in pipelines.items():
        print(f"\n---> Training {name}...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        results[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1 Score': f1
        }
        reports[name] = classification_report(y_test, y_pred, zero_division=0)
        confusion_matrices[name] = confusion_matrix(y_test, y_pred)
        trained_pipelines[name] = pipeline
        
        print(f"{name} Results:")
        print(f"  Accuracy  : {acc:.4f}")
        print(f"  Precision : {prec:.4f}")
        print(f"  Recall    : {rec:.4f}")
        print(f"  F1 Score  : {f1:.4f}")
        print("\nClassification Report:")
        print(reports[name])
        print("Confusion Matrix:")
        print(confusion_matrices[name])
        
    print("\n" + "=" * 60)
    print("STEP 7 — MODEL COMPARISON")
    print("=" * 60)
    
    comparison_df = pd.DataFrame(results).T
    comparison_df = comparison_df[['Accuracy', 'Precision', 'Recall', 'F1 Score']]
    print("\nModel Comparison Table:")
    print(comparison_df.to_string())
    
    # Best model selection strictly based on F1 Score
    best_model_name = comparison_df['F1 Score'].idxmax()
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = results[best_model_name]
    
    print(f"\nBest Model Selected based on F1-Score: {best_model_name}")
    print(f"F1-Score: {best_metrics['F1 Score']:.4f}")
    
    print("\n" + "=" * 60)
    print("STEP 8 — SAVE MODEL & ARTIFACTS")
    print("=" * 60)
    
    os.makedirs('model', exist_ok=True)
    
    model_save_path = os.path.join('model', 'best_model.joblib')
    feature_save_path = os.path.join('model', 'feature_columns.joblib')
    metrics_save_path = os.path.join('model', 'model_metrics.json')
    
    joblib.dump(best_pipeline, model_save_path)
    joblib.dump(feature_cols, feature_save_path)
    
    metrics_payload = {
        'best_model': best_model_name,
        'metrics': {
            'Accuracy': float(best_metrics['Accuracy']),
            'Precision': float(best_metrics['Precision']),
            'Recall': float(best_metrics['Recall']),
            'F1 Score': float(best_metrics['F1 Score'])
        },
        'comparison': {
            k: {m: float(v[m]) for m in v} for k, v in results.items()
        },
        'feature_columns': feature_cols
    }
    
    with open(metrics_save_path, 'w') as f:
        json.dump(metrics_payload, f, indent=4)
        
    print(f"Saved best model to: {model_save_path}")
    print(f"Saved feature columns to: {feature_save_path}")
    print(f"Saved metrics to: {metrics_save_path}")
    
    print("\n" + "=" * 60)
    print("STEP 9 — FEATURE IMPORTANCE / INFLUENCE")
    print("=" * 60)
    
    clf = best_pipeline.named_steps['classifier']
    feature_importance_df = None
    
    if hasattr(clf, 'feature_importances_'):
        importances = clf.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False).reset_index(drop=True)
        print(f"Feature Importances for {best_model_name}:")
        print(feature_importance_df.to_string(index=False))
    elif hasattr(clf, 'coef_'):
        # For Logistic Regression (multi-class has coef_ of shape (n_classes, n_features))
        coefs = clf.coef_
        mean_abs_coef = np.mean(np.abs(coefs), axis=0)
        feature_importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Coefficient Influence (Mean Abs)': mean_abs_coef
        }).sort_values(by='Coefficient Influence (Mean Abs)', ascending=False).reset_index(drop=True)
        print(f"Coefficient-based Feature Influence for {best_model_name}:")
        print(feature_importance_df.to_string(index=False))
    else:
        print("Model does not directly expose feature importances or coefficients.")
        
    print("\n" + "=" * 60)
    print("STEP 10 — TEST SAVED MODEL")
    print("=" * 60)
    
    loaded_model = joblib.load(model_save_path)
    loaded_features = joblib.load(feature_save_path)
    
    test_preds = loaded_model.predict(X_test[loaded_features])
    test_acc = accuracy_score(y_test, test_preds)
    
    print(f"Successfully reloaded model from '{model_save_path}'")
    print(f"Re-calculated accuracy on test set using reloaded model: {test_acc:.4f}")
    assert np.array_equal(test_preds, best_pipeline.predict(X_test)), "Reloaded model predictions mismatch!"
    print("Verification passed! Loaded model predictions match trained pipeline predictions exactly.")
    
    print("\n" + "=" * 60)
    print("STEP 11 — FINAL SUMMARY OUTPUT")
    print("=" * 60)
    
    print(f"Dataset shape              : {df.shape}")
    print(f"Training samples           : {X_train.shape[0]}")
    print(f"Testing samples            : {X_test.shape[0]}")
    print(f"\nModel Comparison:\n{comparison_df.to_string()}")
    print(f"\nBest Model                 : {best_model_name}")
    print(f"Accuracy                   : {best_metrics['Accuracy']:.4f}")
    print(f"Precision                  : {best_metrics['Precision']:.4f}")
    print(f"Recall                     : {best_metrics['Recall']:.4f}")
    print(f"F1-score                   : {best_metrics['F1 Score']:.4f}")
    print(f"\nConfusion Matrix:\n{confusion_matrices[best_model_name]}")
    if feature_importance_df is not None:
        print(f"\nFeature Importance:\n{feature_importance_df.to_string(index=False)}")
    print(f"Saved model path           : {os.path.abspath(model_save_path)}")

if __name__ == "__main__":
    main()
