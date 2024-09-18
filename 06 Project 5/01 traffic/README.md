I initially replicated a model with the following architecture: a 2D convolutional layer with 32 filters, a max-pooling layer, a flattening layer, a dense layer with 128 neurons, and a dropout layer at 50%. This resulted in only 5.3% accuracy. Reducing dropout to 30% dramatically improved accuracy to 92%, with further reductions leading to 94.6% accuracy at 5% dropout. However, overfitting occurred at this point.

I then adjusted the number of neurons, increasing from 128 to 256, which improved accuracy slightly but doubled the computation time. Experiments with two dense layers (128 neurons each) reduced performance to 82.5%.

Next, a second convolutional and max-pooling layer was added, boosting accuracy to 97.6%. Using 64 filters instead of 32 filters marginally increased accuracy to 97.9%, but computation time again doubled.

The final model, with 256 neurons, two convolutional layers (64 filters each), two max-pooling layers, and a 10% dropout rate, yielded similar performance to a simpler version with 32 filters and 128 neurons but with much slower training.