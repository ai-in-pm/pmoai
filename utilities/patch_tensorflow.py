"""
Patch for TensorFlow to redirect contrib.distributions to tensorflow_probability.

This script creates a mock tf.contrib module that redirects distributions
to tensorflow_probability.distributions, which is the modern replacement.
"""

import sys
import types
import builtins

# First, let's try to import tensorflow_probability
try:
    import tensorflow_probability as tfp
    print("Successfully imported tensorflow_probability")
except ImportError:
    print("tensorflow_probability not found. Please install it with:")
    print("pip install tensorflow-probability")
    sys.exit(1)

# Now, let's patch tensorflow
import tensorflow as tf

# Create a mock contrib module if it doesn't exist
if not hasattr(tf, 'contrib'):
    # Create a mock contrib module
    mock_contrib = types.ModuleType('contrib')

    # Set the distributions attribute to point to tfp.distributions
    mock_contrib.distributions = tfp.distributions

    # Add the mock contrib module to tensorflow
    tf.contrib = mock_contrib

    print("Successfully patched TensorFlow with mock contrib module")
    print("tf.contrib.distributions now points to tensorflow_probability.distributions")

print("TensorFlow patch loaded")
