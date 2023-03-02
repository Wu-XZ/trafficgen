import pytorch_lightning as pl
from act.utils.act_dataset import actDataset
import torch.utils.data as data
from torch.utils.data import DataLoader
from utils.config import load_config_act
from act.model.tg_act import actuator
from utils.typedef import AgentType, RoadEdgeType, RoadLineType
import torch
from act.model.tg_act import act_loss
# General config
from pytorch_lightning.loggers import WandbLogger
from utils.config import get_parsed_args
from tqdm import tqdm
import numpy as np
from torch import Tensor

def wash(batch):
    """Transform the loaded raw data to pretty pytorch tensor."""
    for key in batch.keys():
        if isinstance(batch[key], np.ndarray):
            batch[key] = Tensor(batch[key])
        if isinstance(batch[key], torch.DoubleTensor):
            batch[key] = batch[key].float()
        if 'mask' in key:
            batch[key] = batch[key].to(bool)

if __name__ == '__main__':

    args = get_parsed_args()
    cfg = load_config_act(args.config)

    test_set = actDataset(cfg)

    dataloader = DataLoader(
        test_set, batch_size=4, num_workers=0, shuffle=True, drop_last=False
    )


    ade = []
    fde = []
    model = actuator(cfg).load_from_checkpoint('traffic_generator/ckpt/act.ckpt')
    with torch.no_grad():
        for idx, data in enumerate(tqdm(dataloader)):
            pred = model(data)
            loss, loss_dict = act_loss(pred, data)
            ade.append(loss_dict['pos_loss'])
            fde.append(loss_dict['fde'])
    print(np.mean(ade))
    print(np.mean(fde))




