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
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..types import FloatTensor, PandasDataFrame, Tensor


class Store(ABC):
    def __init__(
        self,
        name: str,
        verbose: int = 0,
        **kwargs,
    ):
        """Initializes a Key Value Store for entity metadata.

        Args:
            name: Name of the store.
            verbose: be verbose.
        """
        self.name = name
        self.verbose = verbose

    @abstractmethod
    def add(self, embedding: FloatTensor, label: int | None = None, data: Tensor | None = None) -> int:
        """Add an Embedding record to the key value store.

        Args:
            embedding: Embedding predicted by the model.

            label: Class numerical id. Defaults to None.

            data: Data associated with the embedding. Defaults to None.

        Returns:
            Associated record id.
        """

    @abstractmethod
    def batch_add(
        self,
        embeddings: Sequence[FloatTensor],
        labels: Sequence[int] | None = None,
        data: Sequence[Tensor] | None = None,
    ) -> list[int]:
        """Add a set of embedding records to the key value store.

        Args:
            embeddings: Embeddings predicted by the model.

            labels: Class numerical ids. Defaults to None.

            data: Data associated with the embeddings. Defaults to None.

        See:
            add() for what a record contains.

        Returns:
            List of associated record id.
        """

    @abstractmethod
    def get(self, idx: int) -> tuple[FloatTensor, int | None, Tensor | None]:
        """Get an embedding record from the key value store.

        Args:
            idx: Id of the record to fetch.

        Returns:
            record associated with the requested id.
        """

    @abstractmethod
    def batch_get(self, idxs: Sequence[int]) -> tuple[list[FloatTensor], list[int | None], list[Tensor | None]]:
        """Get embedding records from the key value store.

        Args:
            idxs: ids of the records to fetch.

        Returns:
            List of records associated with the requested ids.
        """

    @abstractmethod
    def size(self) -> int:
        "Number of record in the key value store."

    @abstractmethod
    def save(self, path: Path | str, compression: bool = True) -> None:
        """Serializes index on disk.

        Args:
            path: Directory where to store the data.
            compression: Compress index data. Defaults to True.
        """

    @abstractmethod
    def load(self, path: str) -> int:
        """Load index on disk

        Args:
            path: where to store the data

        Returns:
           Number of records reloaded.
        """

    @abstractmethod
    def to_data_frame(self, num_records: int = 0) -> PandasDataFrame:
        """Export data as a Pandas dataframe.

        Args:
            num_records: Number of records to export to the dataframe.
            Defaults to 0 (unlimited).

        Returns:
            pd.DataFrame: a pandas dataframe.
        """

    @abstractmethod
    def reset(self) -> None:
        """Resets the data in the store."""

    def get_config(self) -> dict[str, Any]:
        """Contains the Store configuration.

        Returns:
            A Python dict containing the configuration of the Store obj.
        """
        config = {
            "name": self.name,
            "verbose": self.verbose,
        }

        return config

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Store:
        """Build a store from a config.

        Args:
            config: A Python dict containing the configuration of the store.

        Returns:
            A distance instance.
        """
        try:
            return cls(**config)
        except Exception as e:
            raise TypeError(
                f"Error when deserializing '{cls.__name__}' using" f"config={config}.\n\nException encountered: {e}"
            )
