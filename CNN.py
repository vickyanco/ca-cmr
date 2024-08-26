import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # First convolutional block: 64 filters
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        
        # Second convolutional block: 128 filters
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        
        # Third convolutional block: 256 filters
        self.conv3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        
        # Fourth convolutional block: 512 filters
        self.conv4 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=2, padding=1)
        self.bn4 = nn.BatchNorm2d(512)
        
        # Global Average Pooling
        self.global_avg_pool = nn.AdaptiveAvgPool2d(1)
        
        # Dropout layer with 0.2 dropout rate
        self.dropout = nn.Dropout(p=0.2)
        
        # Fully connected layer with 16 units
        self.fc1 = nn.Linear(512, 16)
        
        # Final fully connected layer with softmax for binary classification
        self.fc2 = nn.Linear(16, 2)

    def forward(self, x):
        # Pass through the first convolutional block
        x = F.relu(self.bn1(self.conv1(x)))
        
        # Pass through the second convolutional block
        x = F.relu(self.bn2(self.conv2(x)))
        
        # Pass through the third convolutional block
        x = F.relu(self.bn3(self.conv3(x)))
        
        # Pass through the fourth convolutional block
        x = F.relu(self.bn4(self.conv4(x)))
        
        # Apply global average pooling
        x = self.global_avg_pool(x)
        x = x.view(x.size(0), -1)  # Flatten the tensor
        
        # Apply dropout
        x = self.dropout(x)
        
        # Pass through the first fully connected layer
        x = F.relu(self.fc1(x))
        
        # Pass through the final fully connected layer with softmax
        x = F.softmax(self.fc2(x), dim=1)
        
        return x

# Initialize the model
model = CNN()

# Optionally, print the model architecture
print(model)