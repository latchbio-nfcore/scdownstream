
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'ambient_removal': NextflowParameter(
        type=typing.Optional[str],
        default='decontx',
        section_title='Pipeline options',
        description='Specify the tool to use for ambient RNA removal',
    ),
    'doublet_detection': NextflowParameter(
        type=typing.Optional[str],
        default='scrublet',
        section_title=None,
        description='Specify the tools to use for doublet detection.',
    ),
    'doublet_detection_threshold': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='Number of tools that need to agree on a doublet for it to be called as such',
    ),
    'integration_methods': NextflowParameter(
        type=typing.Optional[str],
        default='scvi',
        section_title=None,
        description='Specify the tool to use for integration',
    ),
    'clustering_resolutions': NextflowParameter(
        type=typing.Optional[str],
        default='0.5,1.0',
        section_title=None,
        description='Specify the resolutions for clustering',
    ),
    'celltypist_model': NextflowParameter(
        type=typing.Optional[str],
        default='',
        section_title=None,
        description='Specify the models to use for the celltypist cell type annotation',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

