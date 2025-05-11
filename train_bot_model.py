import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Load your oTree data (exported CSV from a previous run)
df = pd.read_csv('your_otree_export.csv')  # Replace with actual path


# Rename the relevant columns if needed
# Assume you have: participant_id, round_number, player_move, partner_move
# player_move = 1 (cooperate), 0 (defect)

def generate_lagged_features(df, max_lag=4):
    df = df.sort_values(by=['participant_id', 'round_number'])
    for lag in range(1, max_lag + 1):
        df[f'own_action_t-{lag}'] = df.groupby('participant_id')['player_move'].shift(lag)
        df[f'partner_action_t-{lag}'] = df.groupby('participant_id')['partner_move'].shift(lag)
        df[f'both_coop_t-{lag}'] = ((df[f'own_action_t-{lag}'] == 1) & (df[f'partner_action_t-{lag}'] == 1)).astype(int)
        df[f'both_defect_t-{lag}'] = ((df[f'own_action_t-{lag}'] == 0) & (df[f'partner_action_t-{lag}'] == 0)).astype(
            int)
        df[f'you_betrayed_t-{lag}'] = ((df[f'own_action_t-{lag}'] == 0) & (df[f'partner_action_t-{lag}'] == 1)).astype(
            int)
        df[f'you_got_betrayed_t-{lag}'] = (
                    (df[f'own_action_t-{lag}'] == 1) & (df[f'partner_action_t-{lag}'] == 0)).astype(int)

    df = df.dropna().reset_index(drop=True)
    return df


# Generate features
df_features = generate_lagged_features(df, max_lag=4)

# Target is the player's next action
X = df_features.drop(columns=['player_move', 'participant_id', 'round_number', 'partner_move'])
y = df_features['player_move']

# Train/test split (optional, just to check performance)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
model.fit(X_train, y_train)

# Check performance
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model to a file (e.g., to put inside your oTree app)
model_path = os.path.join(os.getcwd(), 'human_like_bot_model.pkl')
joblib.dump(model, model_path)

print(f'Model saved to: {model_path}')
