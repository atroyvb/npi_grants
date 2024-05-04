from tensorflow import keras 
from typing import Iterable 
from keras.losses import MeanSquaredError


def autoencoder(n_input : int, 
                n_bottleneck: int, 
                n_layers: Iterable[int]):
    """Create an autoencoder model with separate encoder, decoder, and complete model for training

    Args:
        n_input (int): the dimensionality of the input data
        n_bottleneck (int): the dimensionality to reduce to 
        n_layers (Iterable[int]): the in-between layers
            Rules:
                1. MUST be descending in size 
                2. no layer may be larger than the input (that's a waste)
                3. let's have some reasonableness about the step sizes
                    it would be weird to say (50,30,29,28,3)
                
    """

    inputs = keras.layers.Input(shape = (n_input, ))  # makes a matrix -- tuple of length 2 
    x = inputs 
    for layer_size in [n_input] + n_layers:
        x = keras.layers.Dense(layer_size, activation = 'relu')(x) # x keeps getting passed in so we create a bunch of layers
    
    bottleneck = keras.layers.Dense(n_bottleneck, activation = 'relu')(x) # gives us the output AND is halfway through both 
    
    dec_inputs = keras.layers.Dense(n_layers[-1], activation = 'relu')(bottleneck)
    y = dec_inputs
    for layer_size in n_layers[:: -1] + [n_input]:
        y = keras.layers.Dense(layer_size, activation = 'relu')(y)



    encoder_model = keras.models.Model(inputs = inputs, outputs = bottleneck)
    full_model = keras.models.Model(inputs = inputs, outputs = y )
    full_model.compile(loss=MeanSquaredError, optimizer = 'adam')

    return encoder_model, full_model

    # encoder_l1 = keras.layers.Dense(encoder[0], activation = 'relu)(inputs)



if __name__ == '__main__':
    from npi_grants.readers import wine_data

    df = wine_data.read()
    labels = df['quality']
    features = df[[col for col in df.columns if col != 'quality']]

    encoder_model, training_model = autoencoder(n_input= 11, 
                                                n_bottleneck= 2, 
                                                n_layers= [8,6,4])
    
    # Min max scaling -- maybe you want to 
    for col in features:
        features[col] -= features[col].min()
        features[col] /= features[col].max() # equivalent to features[col] = features[col]/

    print('Before')
    print(encoder_model.predict(features))

    # An autoencoder is defined as fitting the output data equal to the input data 
    training_model.fit(features.values, features.values, 
                       epochs=50,  # how many times we want to train it, 
                       batch_size = 32, 
                       shuffle = True)

    print('After training')
    print(encoder_model.predict(features))