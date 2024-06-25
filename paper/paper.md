
---
title: 'insert title'
tags:
  - Python
  - metabolomics
  - similarity measure
  - spectral library matching
  - compound identification
  - Cosine correlation
  - Shannon entropy
  - Renyi entropy
  - Tsallis entropy
authors:
  - name: Hunter Dlugas
    orcid: 0000-0002-6819-0045
    equal-contrib: true
    affiliation: "1, 2"
  - name: Seongho Kim
    equal-contrib: true 
    affiliation: "1, 3"
affiliations:
 - name: Wayne State University School of Medicine, USA
   index: 1
 - name: Biostatistics and Bioinformatics Core, Karmanos Cancer Institute
   index: 2
 - name: Biostatistics and Bioinformatics Core, Karmanos Cancer Institute/Department of Oncology
   index: 3
date: 25 June 2024
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

A primary goal of the field of Metabolomics - i.e. the qualitative and quantitative study of metabolites - is to identify chemical compounds comprising a given sample, oftentimes with the motivation of identifying/quantifying biomarkers for use in diagnosing, treating, and/or stratifying the risk of some disease. A central tool for compound identification in Metabolomics is mass spectrometry

In order to assess metabolites (i.e. by-products of metabolism) for their potential in diagnosing, treating, or stratifying the risk of disease

The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration).

# Statement of need

`Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.

# Spectrum Preprocessing Transformations

# Similarity Measures
Given a pair of processed spectra $I=<a_{1},a_{2},...,a_{n}>, J=<b_{1},b_{2},...,b_{n}>\in\mathbb{R}^{n}$, ___ provides functionality for computing the following similarity measures:

* Cosine Similarity Measure:
\begin{equation*}
    S_{Cosine}(I,J)= \frac{I\circ J}{|I|_{2}\cdot |J|_{2}}
\end{equation*}
where multiplication in the numerator refers to the dot product $I\circ J=a_{1}b_{1}+a_{2}b_{2}+...+a_{n}b_{n}$ of $I$ and $J$ and multiplication in the denominator refers to multiplication of the $L^{2}$-norm of $I$ and $J$, $|I|_{2}=\sqrt{a_{1}^{2}+a_{2}^{2}+...+a_{n}^{2}}, |J|_{2}=\sqrt{b_{1}^{2}+b_{2}^{2}+...+b_{n}^{2}}$.

* Shannon Entropy Similarity Measure:
\begin{equation*}
    S_{Shannon}(I,J) = 1-\frac{2\cdot H_{S}\left(\frac{I+J}{2}\right) - H_{S}(I)-H_{S}(J)}{ln(4)}\\
    H_{S}(I)=-\sum_{i=1}^{n}p_{i}\cdot ln(p_{i})
\end{equation*}

* Tsallis Entropy Similarity Measure:
\begin{equation*}
    S_{Tsallis}(I_{q},I_{l},q)=1-\frac{2\times H(I_{Q}/2+I_{L}/2,q)-H(I_{Q},q)-H(I_{L},q)}{N}\\
    N:==\frac{\sum_{i=1}^{n}\left(2\left(\frac{a_{i}}{2}\right)^{q}+2\left(\frac{b_{i}}{2}\right)^{q}-a_{i}^{q}-b_{i}^{q}\right)}{1-q}\\
    H_{T}(I,q)=\frac{\left(\sum_{i=1}^{n}p_{i}^{q}\right)-1}{1-q}\\
    q\neq 1, \ q\textgreater 0
\end{equation*}

* R\'enyi Entropy Similarity Measure:
\begin{equation*}
    S_{Renyi}(I_{Q}, I_{L})=1-\frac{2\times H(I_{Q}/2+I_{L}/2,q)-H(I_{Q},q)-H(I_{L},q)}{N}\\
    N:=\left(\frac{1}{1-q}\right)\left(2\times ln\left(\sum_{i}(a_{i}/2)^{q}+\sum_{j}(b_{j}/2)^{q}\right)-ln(\sum_{i}a_{i}^{q})-ln(\sum_{i}b_{i}^{q})\right)\\
    H(I,q)=\frac{1}{1-q}ln(\sum_{i=1}^{n}p_{i}^{q})\\
    q\neq 1, \ q\textgreater 0
\end{equation*}


Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References

