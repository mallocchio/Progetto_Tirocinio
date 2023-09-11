import ClassifierPrediction
import torch
from typing import List, Tuple

def prediction(tensor):
    """
    Predice i numeri per una lista di immagini rappresentate come tensori utilizzando la funzione 'ClassifierPrediction.prediction'.

    Args:
        tensor (List[torch.Tensor]): Lista di tensori contenenti le immagini da predire.

    Returns:
        List[np.ndarray, torch.Tensor, int]: Una lista di tuple contenenti:
            - np.ndarray: Probabilità predette per ciascun numero (logit).
            - torch.Tensor: Logaritmi delle probabilità predette.
            - int: Numero predetto per ciascuna immagine.
    """
    predictions = ClassifierPrediction.prediction(tensor)
    return predictions