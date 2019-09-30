import pickle
import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

def run_oversampling(input_filename='./dataset/preprocessed_dataset', 
                     label = 'label',
                     strategy = 'minority',
                     output_filename = './dataset/whitened_oversample_dataset'):
    
    df = pd.read_pickle(input_filename)
    df_label =  np.array(df.pop(label)) 

    train, test, train_labels, test_labels = train_test_split(df,
                                             df_label, 
                                             stratify = df_label,
                                             test_size = 0.2, 
                                             random_state = 42)

    # Imputation of missing values
    train = train.fillna(train.mean())
    test = test.fillna(test.mean())
    
    pca = PCA(whiten=True)
    train_whitened = pca.fit_transform(train)
    test_whitened = pca.transform(test)

    # Resample the minority class. You can change the strategy to 'auto' if you are not sure.
    sm = SMOTE(sampling_strategy=strategy, random_state=7)

    # Fit the model to generate the data.
    oversampled_trainX, oversampled_trainY = sm.fit_sample(train_whitened, train_labels)

    divided_dataset = {'train': oversampled_trainX,
                       'test': test_whitened,
                       'train_labels': oversampled_trainY,
                       'test_labels': test_labels,
                       'features' : train.columns
                      }

    with open(output_filename, 'wb') as file:
        pickle.dump(divided_dataset, file)



