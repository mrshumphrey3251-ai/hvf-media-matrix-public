import pathlib
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BaselineResult:
    """Container for baseline statistics."""
    means: pd.Series
    stds: pd.Series
    median: pd.Series
    count: int

    def as_dict(self) -> dict:
        """Return a dictionary representation of the baseline."""
        return {
            "means": self.means.to_dict(),
            "stds": self.stds.to_dict(),
            "median": self.median.to_dict(),
            "count": self.count,
        }


def _validate_columns(df: pd.DataFrame, columns: Optional[Iterable[str]]) -> List[str]:
    """Validate that the requested columns exist in the DataFrame."""
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            raise ValueError("DataFrame contains no numeric columns to compute baseline.")
        return numeric_cols

    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise KeyError(f"The following columns are missing from the DataFrame: {missing}")

    numeric = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]
    if len(numeric) != len(list(columns)):
        non_numeric = set(columns) - set(numeric)
        raise TypeError(f"The following columns are not numeric: {list(non_numeric)}")

    return list(columns)


def calculate_baseline(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    ignore_na: bool = True,
) -> BaselineResult:
    """
    Compute baseline statistics for a given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    columns : iterable of str, optional
        Specific columns to include. If None, all numeric columns are used.
    ignore_na : bool, default True
        Whether to drop NaN values before computation.

    Returns
    -------
    BaselineResult
        Dataclass containing means, standard deviations, medians and row count.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    selected_cols = _validate_columns(df, columns)

    data = df[selected_cols]
    if ignore_na:
        data = data.dropna()

    if data.empty:
        raise ValueError("No data left after NA handling; cannot compute baseline.")

    means = data.mean()
    stds = data.std(ddof=0)  # population std to keep baseline deterministic
    median = data.median()
    count = len(data)

    return BaselineResult(means=means, stds=stds, median=median, count=count)


def load_data(
    source: Union[str, pathlib.Path],
    **read_csv_kwargs,
) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    source : str or pathlib.Path
        Path to the CSV file.
    **read_csv_kwargs : dict
        Additional keyword arguments forwarded to `pd.read_csv`.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    path = pathlib.Path(source)
    if not path.is_file():
        raise FileNotFoundError(f"Unable to locate file: {path}")

    return pd.read_csv(path, **read_csv_kwargs)


def plot_baseline(
    baseline: BaselineResult,
    title: str = "Baseline Statistics",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[Union[str, pathlib.Path]] = None,
) -> plt.Figure:
    """
    Generate a bar plot visualising means and standard deviations.

    Parameters
    ----------
    baseline : BaselineResult
        Baseline statistics to plot.
    title : str, optional
        Plot title.
    figsize : tuple, optional
        Figure size.
    save_path : str or pathlib.Path, optional
        If provided, the figure is saved to this location.

    Returns
    -------
    matplotlib.figure.Figure
        The created figure.
    """
    fig, ax = plt.subplots(figsize=figsize)

    indices = np.arange(len(baseline.means))
    width = 0.35

    ax.bar(
        indices - width / 2,
        baseline.means,
        width,
        yerr=baseline.stds,
        capsize=5,
        label="Mean ± Std",
        color="#2ca02c",
        edgecolor="black",
    )
    ax.set_xticks(indices)
    ax.set_xticklabels(baseline.means.index, rotation=45, ha="right")
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.legend()

    fig.tight_layout()

    if save_path:
        path = pathlib.Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=300)

    return fig


__all__ = [
    "BaselineResult",
    "calculate_baseline",
    "load_data",
    "plot_baseline",
]