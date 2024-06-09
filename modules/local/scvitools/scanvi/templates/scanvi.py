#!/usr/bin/env python3

import scvi
import anndata as ad
from scvi.model import SCVI, SCANVI
import platform

from threadpoolctl import threadpool_limits
threadpool_limits(int("${task.cpus}"))

def format_yaml_like(data: dict, indent: int = 0) -> str:
    """Formats a dictionary to a YAML-like string.

    Args:
        data (dict): The dictionary to format.
        indent (int): The current indentation level.

    Returns:
        str: A string formatted as YAML.
    """
    yaml_str = ""
    for key, value in data.items():
        spaces = "  " * indent
        if isinstance(value, dict):
            yaml_str += f"{spaces}{key}:\\n{format_yaml_like(value, indent + 1)}"
        else:
            yaml_str += f"{spaces}{key}: {value}\\n"
    return yaml_str

adata = ad.read_h5ad("${h5ad}")
model = SCVI.load("${scvi_model}", adata)

n_epochs = int(min([round((20000 / adata.n_obs) * 400), 400]))
n_epochs = int(min([10, max([2, round(n_epochs / 3.0)])]))

model = SCANVI.from_scvi_model(
    scvi_model=model, labels_key="label", unlabeled_category="unknown"
)

model.train(max_epochs=n_epochs, early_stopping=True)
adata.obsm["X_emb"] = model.get_latent_representation()
adata.obs["label:scANVI"] = model.predict()

adata.write_h5ad("${prefix}.h5ad")
adata.obs[["label:scANVI"]].to_pickle("${prefix}.pkl")
model.save("${prefix}_model")

# Versions

versions = {
    "${task.process}": {
        "python": platform.python_version(),
        "anndata": ad.__version__,
        "scvi": scvi.__version__,
    }
}

with open("versions.yml", "w") as f:
    f.write(format_yaml_like(versions))
