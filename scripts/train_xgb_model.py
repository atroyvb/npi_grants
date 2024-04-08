import pandas as pd 

from npi_grants import db, model_features


def create_training_data_features_labels():
    """Load known training data, extract features from db, convert to features. """
    training = pd.read_csv('data/likely_grantee_provider_matchers.csv')
    grantee_ids = ', '.join(training['g_id'])
    query = f'''SELECT last_name, forename, city, state
                FROM grantees
                WHERE is IN ({grantee_ids})'''
    grantees = pd.read_sql(query, db.sql())

    provider_ids = ', '.join
    query = f'''SELECT last_name, forename, city, state
                FROM providers
                WHERE is IN ({provider_ids})'''
    
    feature_extractor = model_features.FeatureExtractor()
    features = feature_extractor.features(grantees, providers)

