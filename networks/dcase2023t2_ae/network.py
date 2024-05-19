import torch
from torch import nn

class AENet(nn.Module):
    def __init__(self,input_dim, block_size):
        super(AENet,self).__init__()
        self.input_dim = input_dim
        self.cov_source = nn.Parameter(torch.zeros(block_size, block_size), requires_grad=False)
        self.cov_target = nn.Parameter(torch.zeros(block_size, block_size), requires_grad=False)

        self.encoder = nn.Sequential(
            nn.Linear(self.input_dim,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,16),
            nn.BatchNorm1d(16,momentum=0.01, eps=1e-03),
            nn.ReLU(),
        )

        self.decoder = nn.Sequential(
            nn.Linear(16,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.BatchNorm1d(256,momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(256,self.input_dim)
        )

    def forward(self, x):
        z = self.encoder(x.view(-1,self.input_dim))
        return self.decoder(z), z
