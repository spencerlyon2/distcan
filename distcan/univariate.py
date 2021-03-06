"""
Univariate distributions

@author : Spencer Lyon <spencer.lyon@stern.nyu.edu>
@date : 2015-01-07

"""
from math import sqrt, log, pi, exp
import numpy as np
import scipy.stats as st
from scipy.special import gamma, gammaln
from .scipy_wrap import CanDistFromScipy

__all__ = ["InverseGamma", "Normal", "Gamma", "NormalInverseGamma", "T",
           "TDist", "F", "FDist", "LogNormal", "Chisq", "Chi2", "Chi",
           "Uniform"]

univariate_class_docstr = r"""
Construct a distribution representing {name} random variables. The pdf
of the distribution is given by

.. math::

    {pdf_tex}

Parameters
----------
{param_list}

Attributes
----------
{param_attributes}
mean :  scalar(float)
    mean of the distribution
std :  scalar(float)
    std of the distribution
var :  scalar(float)
    var of the distribution
skewness :  scalar(float)
    skewness of the distribution
kurtosis :  scalar(float)
    kurtosis of the distribution
median :  scalar(float)
    median of the distribution
mode :  scalar(float)
    mode of the distribution
isplatykurtic :  Boolean
    boolean indicating if d.kurtosis > 0
isleptokurtic :  bool
    boolean indicating if d.kurtosis < 0
ismesokurtic :  bool
    boolean indicating if d.kurtosis == 0
entropy :  scalar(float)
    entropy value of the distribution

"""

param_str = "{name} : {kind}\n    {descr}"


def _create_param_list_str(names, descrs, kinds="scalar(float)"):

    names = (names, ) if isinstance(names, str) else names
    names = (names, ) if isinstance(names, str) else names

    if isinstance(kinds, (list, tuple)):
        if len(names) != len(kinds):
            raise ValueError("Must have same number of names and kinds")

    if isinstance(kinds, str):
        kinds = [kinds for i in range(len(names))]

    if len(descrs) != len(names):
        raise ValueError("Must have same number of names and descrs")

    params = []
    for i in range(len(names)):
        n, k, d = names[i], kinds[i], descrs[i]
        params.append(param_str.format(name=n, kind=k, descr=d))

    return str.join("\n", params)


def _create_class_docstr(name, param_names, param_descrs,
                         param_kinds="scalar(float)",
                         pdf_tex=r"\text{not given}", **kwargs):
    param_list = _create_param_list_str(param_names, param_descrs,
                                        param_kinds)

    param_attributes = str.join(", ", param_names) + " : See Parameters"

    return univariate_class_docstr.format(**locals())

#  -  #
#  T  #
#  -  #


class T(CanDistFromScipy):

    _metadata = {
        "name": "T",
        "pdf_tex": (r"p(x;df)= \frac{1}{\sqrt{df} B\left(\frac{1}{2}, "
                    + r"\frac{df}{2} \right)"
                    + r"\left(1 + \frac{x^2}{df} \right)^{- \frac{df+1}{2}}"
                    + "\n\n" + r"where :math:`B(\cdot)` is the beta function"),

        "cdf_tex": (r"\frac{1}{2} + x \Gamma \left( \frac{df+1}{2}\right)"
                    + r"\frac{2 F_1 \left( \frac{1}{2}, \frac{df+1}{2};"
                    + r"\frac{3}{2}, \frac{-x^2}{df} \right)}"
                    + r"{\sqrt{\pi df} \Gamma \left( \frac{df}{2}\right)}"
                    + "\n\n"
                    + r"where :math:`F_1` is the hypergeometric function"),

        "param_names": ["df"],

        "param_descrs": ["Degrees of freedom (real, >0)"],

        "_str": "T(df=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, df):
        self.df = df

        # set dist before calling super's __init__
        self.dist = st.t(df)
        super(T, self).__init__()

    @property
    def params(self):
        return (self.df,)

TDist = T


#  -  #
#  F  #
#  -  #


class F(CanDistFromScipy):

    _metadata = {
        "name": "F",
        "pdf_tex": (r"p(x; d_1, d_2) = \frac{1}{x B(d_1/2, d_2/2)} "
                    + r"\sqrt{\frac{(d_1 x)^{d_1} \cdot d_2^{d_2}}"
                    + r"{(d_1 x + d_2)^{d_1 + d_2}}}"),

        "cdf_tex": (r"I_{\frac{d_1 x}{d_1 x + d_2}} \left( \frac{d_1}{2},"
                    + r" \frac{d_2}{2} \right)" + "\n\n where :math:`I` "
                    + "is the regularized incomplete beta function"),

        "param_names": ["d1", "d2"],

        "param_descrs": ["Numerator degrees of freedom (must be >0)",
                         "Denominator degrees of freedom (must be >0)"],

        "_str": "F(d1=%.5f, d2=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

        # set dist before calling super's __init__
        self.dist = st.f(d1, d2)
        super(F, self).__init__()

    @property
    def params(self):
        return (self.d1, self.d2)

FDist = F

# ---- #
# Beta #
# ---- #


class Beta(CanDistFromScipy):

    _metadata = {
        "name": "Beta",
        "pdf_tex": (r"p(x; \alpha, \beta) = \frac{1}{B(\alpha, \beta)} "
                    + r"x^{\alpha - 1} (1 - x)^{\beta - 1}, \quad x \in[0, 1]"
                    ),

        "cdf_tex": (r"I_{x}(\alpha, \beta)" + "\n\n where :math:`I` "
                    + "is the incomplete beta function"),

        "param_names": ["d1", "d2"],

        "param_descrs": ["First shape parameter (must be >0)",
                         "Second shape parameter (must be >0)"],

        "_str": "Beta(alpha=%.5f, beta=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

        # set dist before calling super's __init__
        self.dist = st.beta(alpha, beta)
        super(Beta, self).__init__()

    @property
    def params(self):
        return (self.alpha, self.beta)

# --------- #
# LogNormal #
# --------- #


class LogNormal(CanDistFromScipy):

    _metadata = {
        "name": "LogNormal",
        "pdf_tex": (r"p(x; \mu, \sigma) = \frac{1}{x \sqrt{2 \pi \sigma^2}}"
                    + r"\exp \left( - \frac{(\log(x) - \mu)^2}{2 \sigma^2}"
                    + r" \right)"),

        "cdf_tex": (r"\frac{1}{2} + \frac{1}{2} \text{erf} \left["
                    + r"\frac{\log(x) - \mu }{\sqrt{2} \sigma}\right]"),

        "param_names": ["mu", "sigma"],

        "param_descrs": ["Log-scale (mean of log of RV)",
                         "Shape parameter (must be >0, std. of log of RV)"],

        "_str": "LogNormal(mu=%.5f, sigma=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

        # set dist before calling super's __init__
        self.dist = st.lognorm(sigma, scale=exp(mu))
        super(LogNormal, self).__init__()

    @property
    def params(self):
        return (self.mu, self.sigma)

#  ------------  #
#  InverseGamma  #
#  ------------  #


class InverseGamma(CanDistFromScipy):

    _metadata = {
        "name": "InverseGamma",
        "pdf_tex": (r"p(x;\alpha,\beta)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}"
                    + r"x^{-\alpha-1}\exp\left(-\frac{\beta}{x}\right)"),

        "cdf_tex": r"\frac{\Gamma(\alpha, \beta / x)}{\Gamma(\alpha)}",

        "param_names": ["alpha", "beta"],

        "param_descrs": ["Shape parameter (must be >0)",
                         "Scale Parameter (must be >0)"],

        "_str": "InverseGamma(alpha=%.5f, beta=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

        # set dist before calling super's __init__
        self.dist = st.invgamma(alpha, scale=beta)
        super(InverseGamma, self).__init__()

    @property
    def params(self):
        return (self.alpha, self.beta)


#  ------ #
#  Normal #
#  ------ #


class Normal(CanDistFromScipy):

    _metadata = {
        "name": "Normal",
        "pdf_tex": (r"p(x;\mu,\sigma)=\frac{1}{\sigma \sqrt{2\pi}}" +
                    r"e^{-\frac{(x-\mu)^2}{2\sigma^2}}"),

        "cdf_tex": (r"\frac{1}{2} \left[ 1 + \text{erf} " +
                    r"\left( \frac{x-\mu}{\sigma \sqrt{2}}\right)\right]"),

        "param_names": ["mu", "sigma"],

        "param_descrs": ["mean of the distribution",
                         "Standard deviation of the distribution"],

        "_str": "Normal(mu=%.5f, sigma=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

        # set dist before calling super's __init__
        self.dist = st.norm(mu, scale=sigma)
        super(Normal, self).__init__()

    @property
    def params(self):
        return (self.mu, self.sigma)


#  ----- #
#  Gamma #
#  ----- #

class Gamma(CanDistFromScipy):

    _metadata = {
        "name": "Gamma",
        "pdf_tex": (r"p(x;\alpha,\beta)=\frac{x^{\alpha-1}e^{-x/\beta}}" +
                    r"{\Gamma(\alpha)\beta^{\alpha}}"),

        "cdf_tex": (r"\frac{\gamma(\alpha, \beta x)}{\Gamma(\alpha)}" + "\n\n"
                    + r"where :math:`\gamma(\cdot)` is the incomplete"
                    + " gamma function"),

        "param_names": ["alpha", "beta"],

        "param_descrs": ["Shape parameter", "Scale Parameter"],

        "_str": "Gamma(alpha=%.5f, beta=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

        # set dist before calling super's __init__
        self.dist = st.gamma(alpha, scale=beta)
        super(Gamma, self).__init__()

    @property
    def params(self):
        return (self.alpha, self.beta)


#  ----------- #
#  Chi Squared #
#  ----------- #

class Chisq(CanDistFromScipy):

    _metadata = {
        "name": "Chi Squared",
        "pdf_tex": (r"p(x; k)="
                    + r"\frac{x^{k/2 - 1} e^{-x/2}}{2^{k/2} \Gamma(k/2)}"
                    + "\n ;" r"x > 0"),

        "cdf_tex": (r"\frac{1}{\Gamma \left(\frac{k}{2} \right)}" +
                    r"\gamma \left(\frac{k}{2}, \frac{x}{2} \right)"
                    + "\n\n"
                    + r"where :math:`\gamma(\cdot, \cdot)`"
                    + " is the lower incomplete"
                    + " gamma function"),

        "param_names": ["k"],

        "param_descrs": ["Degrees of Freedom"],

        "_str": "ChiSquared(k=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, k):
        self.k = k

        # set dist before calling super's __init__
        self.dist = st.chi2(df=k)
        super(Chisq, self).__init__()

    @property
    def params(self):
        return (self.k)


Chi2 = Chisq


#  --- #
#  Chi #
#  --- #

class Chi(CanDistFromScipy):

    _metadata = {
        "name": "Chi",
        "pdf_tex": (r"p(x; k)=\frac{1}{\Gamma(k/2)} 2^{1 - k/2}"
                    + r"x^{k-1} e^{-x^2 / 2}" + "\n ;" r"x > 0"),

        "cdf_tex": (r"P\left(k/2, x^2/2 \right)"
                    + "\n \n"
                    + "where :math:`P(k, x)` is the regularized Gamma "
                    + "function"),

        "param_names": ["k"],

        "param_descrs": ["Degrees of Freedom"],

        "_str": "Chi(k=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, k):
        self.k = k

        # set dist before calling super's __init__
        self.dist = st.chi(df=k)
        super(Chi, self).__init__()

    @property
    def params(self):
        return (self.k)


# ------- #
# Uniform #
# ------- #

class Uniform(CanDistFromScipy):

    _metadata = {
        "name": "Uniform",
        "pdf_tex": (r"p(x; a, b) = \frac{1}{b-a}; a \leq x \leq b"),

        "cdf_tex": (r"0 \text{ for } x<a"
                    + r"\frac{x-a}{b-a} \text{ for } a \leq x \leq b"
                    + r"1 \text{ for } x > b"),

        "param_names": ["a", "b"],

        "param_descrs": ["Lower Bound", "Upper Bound"],

        "_str": "Uniform(a=%.5f, b=%.5f)"}

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)

    def __init__(self, a, b):
        self.a = a
        self.b = b

        # set dist before calling super's __init__
        self.dist = st.uniform(loc=a, scale=b)
        super(Uniform, self).__init__()

    @property
    def params(self):
        return (self.a, self.b)


# ########################################################################## #
# Below we have other distributions that are not a part of scipy.stats       #
# ########################################################################## #


#  ------------------ #
#  NormalInverseGamma #
#  ------------------ #

# TODO Clean up NIG docstrings

_nig_pdf_doc = r"""
Evaluate the probability density function, which is defined as

.. math::

    {pdf_tex}

Parameters
----------
mu : array_like or scalar(float)
    The mu point(s) (N part of NIG) at which to evaluate the pdf
sig2 : array_like or scalar(float)
    The sigma point(s) (IG part of NIG) at which to evaluate the pdf

Returns
-------
out : {ret1_type}
    The pdf of the distribution evaluated at (mu, sig2) pairs
"""


class NormalInverseGamma(object):

    def __init__(self, mu, v0, shape, scale):
        self.mu = mu
        self.v0 = v0
        self.shape = shape
        self.scale = scale

        # define docstring arguments
        pdf_tex = r"p(x;\alpha,\beta)=\frac{x^{\alpha-1}e^{-x/\beta}}"
        pdf_tex += r"{\Gamma(\alpha)\beta^{\alpha}}"
        cdf_tex = r"\frac{\gamma(\alpha, \beta x)}{\Gamma(\alpha)}" + "\n\n"
        cdf_tex += r"where :math:`\gamma(\cdot)` is the incomplete"
        cdf_tex += " gamma function"

        self._str = "Normal(mu=%.5f, sigma=%.5f, alpha=%.5f, beta=%.5f)"

    def pdf(self, x, sig2):
        m, v, sh, sc = self.mu, self.v0, self.shape, self.scale
        Zinv = sc**sh / gamma(sh) / sqrt(v * 2*pi)
        return (Zinv * 1./(np.sqrt(sig2) * sig2**(sh+1.)) *
                np.exp(-sc/sig2 - 0.5/(sig2*v)*(x-m)**2.0))

    def logpdf(self, x, sig2):
        m, v, sh, sc = self.mu, self.v0, self.shape, self.scale
        lZinv = sh*log(sc) - gammaln(sh) - 0.5*(log(v) + log(2*pi))
        return (lZinv - 0.5*np.log(sig2) - (sh+1.)*np.log(sig2) -
                sc/sig2 - 0.5/(sig2*v)*(x-m)**2)

    @property
    def mode(self):
        return self.mu, self.scale / (self.shape + 1.0)

    @property
    def mean(self):
        sig2 = self.scale / (self.shape - 1.0) if self.shape > 1.0 else np.inf
        return self.mu, sig2

    def _rand1(self):
        sig2 = InverseGamma(self.shape, self.scale).rand()

        if sig2 <= 0.0:
            sig2 = np.finfo(float).resolution  # equiv to julia eps()

        mu = Normal(self.mu, sqrt(sig2 * self.v0)).rand()
        return mu, sig2

    def rand(self, n=1):
        if n == 1:
            return self._rand1()
        else:
            out = np.empty((n, 2))
            for i in range(n):
                out[i] = self._rand1()

            return out


if __name__ == '__main__':
    nig = NormalInverseGamma(0.0, 1.0, 5.0, 6.0)
    print(nig.pdf(1.0, 3.0))
