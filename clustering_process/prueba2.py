

from sklearn.feature_extraction.text import CountVectorizer
train_set = ("The sky is blue.", "The sun is bright.")
test_set = ("The sun in the sky is bright.", "We can see the shining sun, the bright sun.")
count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(train_set)
print("Vocabulary:", count_vectorizer.vocabulary_)
# Vocabulary: {'blue': 0, 'sun': 1, 'bright': 2, 'sky': 3}
freq_term_matrix = count_vectorizer.transform(train_set)
print(freq_term_matrix.todense())