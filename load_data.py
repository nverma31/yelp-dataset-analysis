'''
Script to load data from file. The exact columns to load should
be specified.
----------
'''
from gensim import corpora, models, similarities
import pandas as pd
import simplejson as json
from datetime import datetime
import nltk
from nltk.corpus import stopwords
import itertools
from sklearn.cross_validation import train_test_split

print '**Loading data...'

# LOAD DATA FOR TYPE = dataset_type
fileheading = '/Users/Neeraj/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_'

def get_data(line, cols):
    d = json.loads(line)
    return dict((key, d[key]) for key in cols)

# Load business data
cols = ('business_id', 'name', 'categories', 'city', 'latitude', 'longitude')
with open(fileheading + 'business.json') as f:
    df_business = pd.DataFrame(get_data(line, cols) for line in f)
df_business = df_business.sort('business_id')
df_business.index = range(len(df_business))
df_business.info()


# Load review data
cols = ('user_id', 'business_id', 'stars','text')
with open(fileheading + 'review.json') as f:
    df_review = pd.DataFrame(get_data(line, cols) for line in f)
df_review.info()
# print(df_review[df_review.business_id == df_business.business_id[(df_business.city == 'Pittsburgh')|(df_business.city == 'Carnegie')]])
df_pitt = (df_review[df_review['business_id'].isin(df_business.business_id[(df_business.city == 'Pittsburgh')|(df_business.city == 'Carnegie')])])
# documents = dfList
# texts = [[word for word in document.lower().split() if word not in stopwords] for document in documents]
# dictionary = corpora.Dictionary(texts)
# corpus = [dictionary.doc2bow(text) for text in texts]
# #
# lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=5)
# print lda.print_topics(5)
data_load_time = datetime.now()
d = pd.merge(df_pitt, df_business, on='business_id', how='inner')
print d.info()
print 'Data was loaded at ' + data_load_time.time().isoformat()
