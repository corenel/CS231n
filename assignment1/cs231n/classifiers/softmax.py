import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  num_train = X.shape[0]
  num_class = W.shape[1]

  for i in range(num_train):
    # L_i = -f_{y_i} + \log\sum_j e^{f_j}
    # f(x_i; W) =  W x_i
    f = X[i].dot(W)
    # Shift the values of f so that the highest number is 0
    # To improve the numerical stability of the computation
    f -= np.max(f)
    p = np.sum(np.exp(f))
    loss += -f[y[i]] + np.log(p)

    dW[:, y[i]] -= X[i]
    for j in range(num_class):
      dW[:, j] += (np.exp(f[j]) / p)  * X[i]

  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg * W


  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]

  f = X.dot(W)
  f -= np.max(f, axis=1, keepdims=True)
  p  = np.exp(f) / np.sum(np.exp(f), axis=1, keepdims=True)

  loss = np.sum(-np.log(p[np.arange(num_train), y]))

  p_mask = np.zeros_like(p)
  p_mask[np.arange(num_train), y] = 1
  dW = X.T.dot(p - p_mask)

  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

