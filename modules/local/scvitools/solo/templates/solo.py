#!/usr/bin/env python3

import scvi
import anndata as ad
from scvi.model import SCVI
from scvi.external import SOLO
import platform

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

setup_kwargs = {"layer": "counts", "batch_key": "${meta.batch_col}"}

# Defaults from SCVI github tutorials scanpy_pbmc3k and harmonization
model_kwargs = {
    "gene_likelihood": "nb",
    "n_layers": 2,
    "n_hidden": 128,
    "n_latent": 30,
}

train_kwargs = {"train_size": 1.0}

n_epochs = int(min([round((20000 / adata.n_obs) * 400), 400]))

SCVI.setup_anndata(adata, **setup_kwargs)
model = SCVI(adata, **model_kwargs)
model.train(max_epochs=n_epochs, **train_kwargs)

if "${meta.label_col}":
    from scvi.model import SCANVI

    n_epochs = int(min([10, max([2, round(n_epochs / 3.0)])]))

    model = SCANVI.from_scvi_model(scvi_model = model, labels_key = "${meta.label_col}", unlabeled_category = "Unknown")
    model.train(max_epochs=n_epochs, **train_kwargs)

adata.obs["singlet"] = False

for batch in adata.obs["${meta.batch_col}"].unique():
    solo = SOLO.from_scvi_model(model, restrict_to_batch=batch)
    solo.train()
    result = solo.predict(False)

    singlets = result[result == "singlet"].index.tolist()
    adata.obs.loc[singlets, "singlet"] = True

adata = adata[adata.obs["singlet"]].copy()
adata.obs.drop("singlet", axis=1, inplace=True)

adata.write_h5ad("${prefix}.h5ad")

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