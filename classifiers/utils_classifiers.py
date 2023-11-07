from tensorflow.keras.datasets import mnist
import torch
import numpy as np
from classifiers.classifiers import TF_LeNet1, TF_LeNet4, TF_LeNet5, Torch_LeNet1, Torch_LeNet4, Torch_LeNet5

def train_model(model_name, img_rows, img_cols):
    model_constructors = {
        "lenet1": TF_LeNet1,
        "lenet4": TF_LeNet4,
        "lenet5": TF_LeNet5,
        # per aggiungere un modello inseriscilo qui
    }

    if model_name not in model_constructors:
        raise ValueError("Model name not supported")

    tf_model = model_constructors[model_name](train=True, img_rows=img_rows, img_cols=img_cols)

    model_converter = {
        "lenet1": Torch_LeNet1,
        "lenet4": Torch_LeNet4,
        "lenet5": Torch_LeNet5,
        # per aggiungere un modello inseriscilo qui
    }
    torch_model = model_converter[model_name]()
    convert_tf_to_torch(tf_model, torch_model, model_name, img_rows, img_cols)

def convert_tf_to_torch(tf_model, torch_model, model_name, img_rows, img_cols):
    img_dim = img_rows * img_cols
    input_shape = (img_rows, img_cols, 1)

    tf_weights = tf_model.get_weights()

    # load pt state_dict
    net = torch_model
    sd = net.state_dict()


    # copy tf weights to pt
    def translate_convw(weights, index):
        convw = weights[index]
        convw = np.transpose(convw, (3, 2, 0, 1))
        convw = torch.from_numpy(convw)
        return convw

    def translate_outw(weights, index):
        outw = weights[index]
        outw = np.transpose(outw)
        outw = torch.from_numpy(outw)
        return outw

    def translate_bias(weights, index):
        convb = weights[index]
        convb = torch.from_numpy(convb)
        return convb


    sd['conv1.weight'] = translate_convw(tf_weights, 0)
    sd['conv1.bias'] = translate_bias(tf_weights, 1)
    sd['conv2.weight'] = translate_convw(tf_weights, 2)
    sd['conv2.bias'] = translate_bias(tf_weights, 3)

    if model_name == "lenet1":

        sd['out.weight'] = translate_outw(tf_weights, 4)
        sd['out.bias'] = translate_bias(tf_weights, 5)

    elif model_name == "lenet4":

        sd['fc1.weight'] = tranlate_outw(tf_weights, 4)
        sd['fc1.bias'] = translate_bias(tf_weights, 5)

        sd['out.weight'] = translate_outw(tf_weights, 6)
        sd['out.bias'] = translate_bias(tf_weights, 7)

    elif model_name == "lenet5":

        sd['fc1.weight'] = translate_outw(tf_weights, 4)
        sd['fc1.bias'] = translate_bias(tf_weights, 5)

        sd['fc2.weight'] = translate_outw(tf_weights, 6)
        sd['fc2.bias'] = translate_bias(tf_weights, 7)

        sd['out.weight'] = translate_outw(tf_weights, 8)
        sd['out.bias'] = translate_bias(tf_weights, 9)

    torch.save(sd, "./trained/" + f"{model_name}.pt")

def load_model(model_name, model_path, input_tensor=None, device=None):

    if input_tensor is None:
        model_constructors = {
            "lenet1": Torch_LeNet1,
            "lenet4": Torch_LeNet4,
            "lenet5": Torch_LeNet5,
        }

        if model_name not in model_constructors:
            raise ValueError("Model name not supported")

    
        model = model_constructors[model_name]()
        model.load_state_dict(torch.load(model_path))
        model.eval()

    else:
        model_constructors = {
            "lenet1": TF_LeNet1,
            "lenet4": TF_LeNet4,
            "lenet5": TF_LeNet5,
        }

        if model_name not in model_constructors:
            raise ValueError("Model name not supported")
        
        model = model_constructors[model_name](input_tensor=input_tensor, model_path=model_path)

    return model

