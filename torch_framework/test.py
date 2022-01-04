import numpy as np
import torch
import torch.nn.functional as F

# for each different type of picture predict classes
def sample_random_cl(label,dataset):
  mask = (dataset.targets == label).cpu().numpy()
  idx = np.where(mask == True)[0]
  rnd_idx = np.random.choice(idx,1)[0]
  return dataset[rnd_idx][0], dataset[rnd_idx][1]


def predict_soft(image,model,device):
  model.eval()
  image = image.unsqueeze(0)
  with torch.no_grad():
    y_hat = model(image.to(device))
    y_hat = F.softmax(y_hat,dim = 1).cpu().numpy()
  return y_hat

def predict_cl(test_loader,model,device):
  y_hat = np.array([],dtype = "int")
  y_true = np.array([],dtype = "int")
  model.eval()
  with torch.no_grad():
    for x,y in test_loader:
      pred = model(x.to(device)).cpu().numpy()
      pred = np.argmax(pred,axis = 1)
      y_hat = np.concatenate((y_hat,pred))
      y_true = np.concatenate((y_true,y))
  return y_true, y_hat

def get_confusion(y_true,y_hat):
  n_labs = len(np.unique(y_true))
  cm = np.zeros((n_labs,n_labs))
  for true, pred in zip(y_true,y_hat):
    cm[true,pred] += 1
  return cm

def get_precision_cl(cm,lab_dict):
  names = list(lab_dict.values())
  share_correct = np.diag(cm) / np.sum(cm,axis = 1)
  print("Precision for each class")
  print("")
  for lab,share in zip(names,share_correct):
    print(f"{lab}\t\t{share*100:.2f} %")
  print("")
  acc = np.sum(np.diag(cm)) / np.sum(cm)
  print(f"Overall accuracy\t{acc*100:.2f} %")