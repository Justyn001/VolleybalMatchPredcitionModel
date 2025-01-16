import torch
from torch import nn
from torchmetrics import Accuracy
from sklearn.model_selection import train_test_split
from data import prepare_data

device = "cuda" if torch.cuda.is_available() else "cpu"

X, Y  = prepare_data()
print(X.shape)

numpy_array_X, numpy_array_Y = X.values, Y.values

X = torch.from_numpy(numpy_array_X).type(torch.float)
Y = torch.from_numpy(numpy_array_Y).type(torch.float)

print(X)

x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=42)

x_train, x_test = x_train.to(device), x_test.to(device)
y_train, y_test = y_train.to(device), y_test.to(device)

print(len(x_train), len(y_train))

class VolleyballModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(in_features=42, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=1),
        )

    def forward(self, x:torch.Tensor) -> torch.Tensor:
        return self.linear_layer_stack(x)

torch.manual_seed(42)
torch.cuda.manual_seed(42)
model_1 = VolleyballModel().to(device)

epoches = 1000

loss_function = torch.nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(params=model_1.parameters(),
                             lr=0.01)

accuracy = Accuracy(task='binary', num_classes=2).to(device)

for epoch in range(epoches):
    model_1.train()
    y_logits = model_1(x_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits))
    train_accuracy = accuracy(y_pred, y_train)
    loss = loss_function(y_logits, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    model_1.eval()
    with torch.inference_mode():
        y_test_logits = model_1(x_test).squeeze()
        y_pred_test = torch.round(torch.sigmoid(y_test_logits))
        test_accuracy = accuracy(y_pred_test, y_test)
        loss_test = loss_function(y_test_logits, y_test)
        if epoch % 10 == 0:
            print(f"Epoch: {epoch} | Train loss: {loss:.5f} | Train accuracy: {train_accuracy * 100:.2f} | Test loss: "
                  f"{loss_test:.5f} | Test accuracy {test_accuracy * 100:.2f}")
    
