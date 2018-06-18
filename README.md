# SimDial
Synthetic Task-oriented Dialog Generator with controllable complexity. This is the dialog data used 
by our SIGDIAL 2018 paper: [Zero-Shot Dialog Generation with Cross-Domain Latent Actions](https://arxiv.org/abs/1805.04803). S
See paper for details.

## Prerequisites
 - Python 2.7
 - Numpy
 - NLTK
 - progressbar
 
 
## Usage 
Run the following code to generate dialog data for multiple domains that are defined in the 
*multiple_domains.py* script. 
  
    python multiple_domains.py
    
The data will be saved into two folders
     
    test/ for testing data 
    train/ for training data

## References
   If you use any source codes or datasets included in this toolkit in your work, please cite the following paper. The bibtex are listed below:
   
    @article{zhao2018zero,
      title={Zero-Shot Dialog Generation with Cross-Domain Latent Actions},
      author={Zhao, Tiancheng and Eskenazi, Maxine},
      journal={arXiv preprint arXiv:1805.04803},
      year={2018}
    }
