import torch
import lightning as L
from torch.utils.data import DataLoader, random_split
from torcheval.metrics import BinaryAccuracy

from src.dataset import DuelsDataset
from src.parser import parse_res


class LSTMClassifier(L.LightningModule):
    def __init__(self, feature_size: int, hidden_dim: int = 256, num_layers: int = 4):
        super().__init__()
        self.attacker_lstm = torch.nn.LSTM(feature_size, hidden_dim, batch_first=True, num_layers=num_layers)
        self.defender_lstm = torch.nn.LSTM(feature_size, hidden_dim, batch_first=True, num_layers=num_layers)
        self.linear = torch.nn.Linear(hidden_dim * 2, 1)

    def forward(self, attacker, defender):
        _, (attacker_hidden, _) = self.attacker_lstm(attacker)
        _, (defender_hidden, _) = self.defender_lstm(defender)

        hidden = torch.cat([attacker_hidden[-1], defender_hidden[-1]], dim=-1)
        logit = self.linear(hidden).squeeze()
        return logit

    def training_step(self, batch, batch_idx):
        attacker, defender, y = batch
        outputs = self(attacker, defender)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(outputs, y.float())
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.002)


def main(res: str, window_length: int = 128):
    attacker_df, defender_df, labels = parse_res(res, window_length=window_length)

    # TODO: drop strings for now, figure out how to one-hot encode later
    attacker_df = attacker_df.drop(["map_name"], axis="columns")
    defender_df = defender_df.drop(["map_name"], axis="columns")

    dataset = DuelsDataset(attacker_df, defender_df, labels)
    train_dataset, test_dataset = random_split(dataset, [0.8, 0.2], generator=torch.Generator().manual_seed(0))

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64)

    model = LSTMClassifier(feature_size=9).float()

    trainer = L.Trainer(max_epochs=200)
    trainer.fit(model, train_loader)

    model.eval()

    accuracy = BinaryAccuracy(threshold=0.5)
    for attacker, defender, y in train_loader:
        y_hat = model(attacker, defender)
        accuracy.update(y_hat, y)
    print("train", accuracy.compute())

    accuracy = BinaryAccuracy()
    for attacker, defender, y in test_loader:
        y_hat = model(attacker, defender)
        accuracy.update(y_hat, y)
    print("test", accuracy.compute())


if __name__ == "__main__":
    main("../../res/dem")
