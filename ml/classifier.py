import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.models import Sequential, Model
from keras.layers import Embedding, LSTM, SimpleRNN, Dense, Input, concatenate, Reshape
from keras.optimizers import Adam
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dropout
from keras.callbacks import ReduceLROnPlateau  # Import ReduceLROnPlateau

# Load the data from "word_lists.csv"
data = pd.read_csv('/Users/abhinavgoel/Downloads/combined_word_lists.csv')
category_mapping = {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2}
data['categories'] = data['categories'].map(category_mapping)

# Split the data into features (word_lists), categories, and names
X_text = data["word_lists"]
X_nutrition = data["nutrition"]
y_categories = data["categories"]
y_names = data["name"]

# Split the data into training and testing sets for categories
X_text_train, X_text_test, X_nutrition_train, X_nutrition_test, y_categories_train, y_categories_test = train_test_split(
    X_text, X_nutrition, y_categories, test_size=0.2, random_state=42
)

# Initialize a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust the number of features as needed

# Transform text data to TF-IDF features
X_text_train_tfidf = tfidf_vectorizer.fit_transform(X_text_train)
X_text_test_tfidf = tfidf_vectorizer.transform(X_text_test)

# Convert TF-IDF matrices to NumPy arrays
X_text_train_tfidf = X_text_train_tfidf.toarray()
X_text_test_tfidf = X_text_test_tfidf.toarray()

# Tokenize and pad sequences for text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_text_train)
X_text_train_seq = tokenizer.texts_to_sequences(X_text_train)
X_text_test_seq = tokenizer.texts_to_sequences(X_text_test)
X_text_train_padded = pad_sequences(X_text_train_seq)
X_text_test_padded = pad_sequences(X_text_test_seq, maxlen=X_text_train_padded.shape[1])

# Preprocess and normalize nutrition data
X_nutrition_train = X_nutrition_train.apply(lambda x: [float(val) for val in x.strip('[]').split(',')])
X_nutrition_test = X_nutrition_test.apply(lambda x: [float(val) for val in x.strip('[]').split(',')])

# Define the LSTM model for text data
text_input = Input(shape=(X_text_train_padded.shape[1],))
text_embedding = Embedding(input_dim=5000, output_dim=256)(text_input)
text_lstm = LSTM(256)(text_embedding)

# Define the SimpleRNN model for nutrition data
nutrition_input = Input(shape=(7,))
nutrition_reshaped = Reshape((1, 7))(nutrition_input)  # Reshape to match SimpleRNN input shape
nutrition_rnn = SimpleRNN(256)(nutrition_reshaped)

# Concatenate text and nutrition data
combined_input = concatenate([text_lstm, nutrition_rnn])

# Add more hidden layers
x = Dense(256, activation='relu')(combined_input)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)

# Add a fully connected layer for classification
output_layer = Dense(3, activation='softmax')(x)  # 3 classes for Breakfast, Lunch, Dinner

# Create the multi-input model
model = Model(inputs=[text_input, nutrition_input], outputs=output_layer)

# Define the learning rate scheduler
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Training with learning rate scheduler
model.fit([X_text_train_padded, np.array(X_nutrition_train.tolist())], y_categories_train, batch_size=20, epochs=10, 
          verbose=1, validation_data=([X_text_test_padded, np.array(X_nutrition_test.tolist())], y_categories_test), 
          callbacks=[reduce_lr])

# Evaluation
y_categories_pred = model.predict([X_text_test_padded, np.array(X_nutrition_test.tolist())])
y_categories_pred_classes = np.argmax(y_categories_pred, axis=1)
accuracy = accuracy_score(y_categories_test, y_categories_pred_classes)
print(f"Category Prediction Accuracy: {accuracy}")
# Save the model
model.save('/Users/abhinavgoel/Downloads/secondModelNutrition.h5')

# Save the tokenizer
with open('/Users/abhinavgoel/Downloads/tokenizer2.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)
