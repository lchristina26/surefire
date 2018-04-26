import torch
from torch.nn import Module, ReLU, ModuleList, Linear

from surefire.modules import Combine, LinearBlock


class ConcatNet(Module):
    def __init__(self, features, out_features, layers=[], activation=ReLU):
        super().__init__()
        self._combine = Combine(features)
        self._blocks = ModuleList()
        num_in = self._combine.out_features
        in_features = num_in
        for num_out in layers:
            self._blocks.append(LinearBlock(num_in, num_out, activation))
            in_features += num_out
            num_in = num_out
        self._final = Linear(in_features, out_features)
        
    def forward(self, x):
        features = [self._combine(x)]
        for block in self._blocks:
            features.append(block(features[-1]))
        return self._final(torch.cat(features, dim=1))
