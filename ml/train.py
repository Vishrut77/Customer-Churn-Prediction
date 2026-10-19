import pandas as pd
from pathlib import Path
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



#______________________Data Preparing for Random Forest_______________________________#

# loading cleaned dataset
script_dir = os.path.dirname(__file__) 
file_path = os.path.join(script_dir, 'Cleaned_Customer_churn.csv')
data = pd.read_csv(file_path)

# Drop Unnamed: 0 index column if present
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"])

# separating features (X) and target feature (Y)
X = data.drop(columns="Churn")

Y = data["Churn"]

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

#now applyinh OneHotEncoder for categorical data where binary type representation is not possible 
# OneHotEncoder(OHE): Converts categorical text values into separate binary (0/1) columns.
# ColumnTransformer: Applies different preprocessing operations to specified columns while handling the remaining columns as configured.

# The only columns needing One-Hot Encoding
categorical_cols = ["InternetService", "Contract", "PaymentMethod"]

# Created a transformer that applies One-Hot Encoding to selected columns
encoder = ColumnTransformer(
    transformers=[
        (
            "encoder", # Name given to this transformation
            OneHotEncoder(handle_unknown="ignore"),# Convert categories into 0s and 1s.# Ignore categories not seen during training.
            categorical_cols # Apply One-Hot Encoding only to these columns
        )
        ],remainder="passthrough" # Keep all other columns unchanged
)


# Learns categories and converts training data into numbers
x_train = encoder.fit_transform(x_train)

# Applies the same conversion to test data
x_test = encoder.transform(x_test)


#___________________________Training Random Forest_________________________________#

# Initialize the Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)

rf.fit(x_train, y_train)

# Predict on test data
prediction = rf.predict(x_test)

accuracy = accuracy_score(y_test, prediction)

print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")


#before effectively aapplying OHE the accuracy was 75% and total column become(18->43)
#after applying OHE and replacing vlaue to 0 and 1 in data cleaning phase so OHE applied only on 3 columns instead of all columns 
# so now aaccuracy is 79.27 and total column is 25 not 43

#exporting model as joblib
PROJECT_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = PROJECT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "churn_pipeline.joblib"

# Save the encoder, trained model, and input column names
joblib.dump(
    {
        "encoder": encoder,
        "model": rf,
        "input_columns": X.columns.tolist()
    },
    MODEL_PATH
)