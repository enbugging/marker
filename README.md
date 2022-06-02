# Introduction
Marker is a Python module aiming for improving readability of text, in particular long and/or dense text and for audience with dyslexia condition. It is not designed to be an accurate highlighter, but to work fast and with streams of text, intended for further development.

The project combines several ideas, to which we owe my acknowledgement:
- Bionic Reading, shared on LinkedIn by Mathis Grosjean,
- Typoglycemia, now allegedly credited to Graham Rawlinson, who did his PhD. on the topic in 1976,
- PositionRank, a keyword extraction method invented by Corina Florescu and Cornelia Caragea. (Florescu, C., & Caragea, C. (2017). A Position-Biased PageRank Algorithm for Keyphrase Extraction. Proceedings of the AAAI Conference on Artificial Intelligence, 31(1). https://doi.org/10.1609/aaai.v31i1.11082)

# Installation
## Dependencies
- Python (>= 3.8)
- Numpy (>=1.17.3)
- NTLK (>= 3.7)

## User installation
With a working installation of numpy, the easiest way to install is by using `pip` 
```
pip install marker
```
# Source code
The latest source is available with 
```
git clone https://github.com/enbugging/marker.git
```