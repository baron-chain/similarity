# Copyright 2021 The TensorFlow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"Collection of specialized notebook vizualization tools"
import importlib.util

excs = []
for mod in ["PIL", "umap", "bokeh", "distinctipy", "matplotlib"]:
    if importlib.util.find_spec(mod) is None:
        excs.append(
            ModuleNotFoundError(
                f"{mod} is not installed. Please install it with `pip install tensorflow_similarity[visualization]`"
            )
        )

if excs:
    raise Exception(excs)
else:
    from .confusion_matrix_viz import confusion_matrix  # noqa
    from .neighbors_viz import viz_neigbors_imgs  # noqa
    from .projector import projector  # noqa
    from .vizualize_views import visualize_views  # noqa
