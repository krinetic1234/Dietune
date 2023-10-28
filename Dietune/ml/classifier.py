import pandas as pd
import nltk
from nltk.corpus import wordnet
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from nltk.stem import WordNetLemmatizer

data = pd.read_csv('PycharmProjects/CalHacksNutritionProj/hundred_filtered_cleaned_data.tsv', sep='\t')

data['full_text'] = data['product_name'] + ' ' + data['ingredients_text']

# Define a function to convert Part of Speech (POS) tags to WordNet POS format
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun

# Lemmatize text using NLTK
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
    return ' '.join(lemmatized_words)

# Apply lemmatization to the 'full_text' column
data['full_text'] = data['full_text'].apply(lemmatize_text)

# Remove duplicate column 'proteins_100g'
X = data[['full_text', 'energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'calcium_100g']]
y = data['categories']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

text_transformer = Pipeline([
    ('tfidf', TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        token_pattern=r'\b\w+\b',
    )),
])

numeric_transformer = Pipeline([
    ('scaler', StandardScaler()),
])

# Define a column transformer to apply the respective transformers to the text and numeric data
preprocessor = ColumnTransformer(
    transformers=[
        ('text', text_transformer, 'full_text'),
        ('numeric', numeric_transformer, ['energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'calcium_100g'])
    ]
)

# Create a classifier with the best hyperparameters
classifier = Pipeline([
    ('preprocessor', preprocessor),
    ('clf', RandomForestClassifier(max_depth=26, min_samples_split=2, n_estimators=280)),
])

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
grouped_data = data.groupby('categories')
summary_statistics = grouped_data[['energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'calcium_100g']].describe()

print("Classifier Accuracy:", accuracy)
print("Classifier Report:")
print(report)