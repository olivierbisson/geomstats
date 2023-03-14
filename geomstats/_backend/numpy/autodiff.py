"""Placeholders with error messages.

NumPy backend does not offer automatic differentiation.
The following functions return error messages.
"""

_USE_OTHER_BACKEND_MSG = (
    "Automatic differentiation is not supported with numpy backend. "
    "Use autograd or pytorch backend instead.\n"
    "Change backend via the command "
    "export GEOMSTATS_BACKEND=autograd in a terminal."
)


def detach(x):
    """Return a new tensor detached from the current graph.

    This is a placeholder in order to have consistent backend APIs.

    Parameters
    ----------
    x : array-like
        Tensor to detach.
    """
    return x


def value_and_grad(*args, **kwargs):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def jacobian(func):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def jacobian_vec(func, point_ndim=1):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def hessian(func):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def hessian_vec(func):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def jacobian_and_hessian(func):
    """Return an error when using automatic differentiation with numpy."""
    raise RuntimeError(_USE_OTHER_BACKEND_MSG)


def custom_gradient(*grad_funcs):
    """Decorate a function to define its custom gradient(s).

    This is a placeholder in order to have consistent backend APIs.
    """

    def decorator(func):
        return func

    return decorator
