#!/usr/bin/env python3
"""
Script to calculate the celestial positions of planets
"""

import pandas as pd
import numpy as np
from astropy.time import Time
from astropy.coordinates import get_body_barycentric, solar_system_ephemeris, SphericalRepresentation
from astropy import units as u
from typing import Optional
import logging
import warnings
import pickle
from functools import partial
from pathlib import Path
from joblib import Memory

# Define a logger for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Ephemeris:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.cache_dir = self.base_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.memory = Memory(self.cache_dir, verbose=0)
        self.ephemeris_path = str(self.base_dir / 'de440.bsp')

    def _cached_heliocentric_longitudes(self, time: Time, body: str) -> Optional[float]:
        """
        Calculates heliocentric longitude for a planet from a given start date.
        Tries builtin first (lightest), then 'de440' if needed.
        """
        ephemeris_sources = ['builtin', 'de440']
        for i, source in enumerate(ephemeris_sources):
            try:
                with solar_system_ephemeris.set(source):
                    t = Time(time)
                    pos = get_body_barycentric(body, t) - get_body_barycentric('sun', t)
                    return SphericalRepresentation.from_cartesian(pos).lon.to(u.deg).value
            except Exception as e:
                if i < len(ephemeris_sources) - 1:
                    logger.warning(f"Failed with {source} for {body} on {time} due to {e}. Trying next fallback.")
                else:
                    logger.error(f"Failed to get longitudes for {body} with all sources.")
                    raise

    # Add caching to the instance method
    _cached_heliocentric_longitudes = property(lambda self: self.memory.cache(self._cached_heliocentric_longitudes))
    
    def get_heliocentric_longitude(self, time: Time, body: str) -> Optional[float]:
        """
        Get heliocentric longitude for a given date and body
        """
        try:
            logger.debug(f"Calculating longitude for {body} on {time}")
            return self._cached_heliocentric_longitudes(time, body)
        except Exception:
            return None

    def get_heliocentric_longitudes_vectorized(self, dates, body: str):
        """
        Calculates heliocentric longitudes for a planet for an array of dates.
        Tries builtin first, then 'de440'.
        """
        ephemeris_sources = ['builtin', 'de440']
        for i, source in enumerate(ephemeris_sources):
            try:
                with solar_system_ephemeris.set(source):
                    times = Time(dates)
                    pos = get_body_barycentric(body, times) - get_body_barycentric('sun', times)
                    return SphericalRepresentation.from_cartesian(pos).lon.to(u.deg).value
            except Exception as e:
                if i < len(ephemeris_sources) - 1:
                    logger.warning(f"Vectorized calculation failed with {source} for {body} due to {e}. Trying next fallback.")
                else:
                    logger.error(f"Failed to get longitudes for {body} with all sources.")
                    raise
    
    def calculate_longitudes_and_synodic_angles(self, start: str, end: str, bodies: list, step: float = 7) -> pd.DataFrame:
        """
        Calculate heliocentric longitudes for a list of bodies and synodic angles between each pair over a time period.
        Returns a DataFrame with columns for each body's longitude and each pair's synodic angle.
        """
        dates = pd.date_range(start=start, end=end, freq=f'{step}D')
        if dates.empty or not bodies:
            return pd.DataFrame()

        # Calculate longitudes for all bodies
        longitudes = {}
        for body in bodies:
            try:
                longitudes[body] = self.get_heliocentric_longitudes_vectorized(dates, body)
            except Exception as e:
                logger.warning(f"Failed to get longitude for {body}: {e}")
                longitudes[body] = np.full(len(dates), np.nan)

        df = pd.DataFrame(longitudes, index=dates)
        df.dropna(inplace=True)
        if df.empty:
            return pd.DataFrame()

        # Calculate synodic angles for each unique pair
        from itertools import combinations
        for body1, body2 in combinations(bodies, 2):
            angle_diff = np.abs((df[body2] - df[body1]) % 360)
            synodic_angle = np.minimum(angle_diff, 360 - angle_diff)
            col_name = f"{body2}-{body1}_synodic"
            df[col_name] = synodic_angle

        return df

    def calculate_synodic_period(
            self,
            start: str,
            end: str,
            body_1: Optional[str] = None,
            body_2: Optional[str] = None,
            bodies: Optional[list] = None,
            step: float = 7
    ) -> pd.DataFrame:
        """
        Calculate the angular separation between two planets over a time period.

        Backwards-compatible API:
        - If `bodies` is provided (list of names), returns longitudes for each body
          and synodic angles for each unique pair (uses
          `calculate_longitudes_and_synodic_angles`).
        - Otherwise expects `body_1` and `body_2` and returns the pairwise
          synodic DataFrame (original behaviour, with caching).
        """
        # If user supplied a list of bodies, delegate to the multi-body method
        if bodies:
            if not isinstance(bodies, (list, tuple)) or len(bodies) < 2:
                raise ValueError("`bodies` must be a list/tuple with at least two names")
            return self.calculate_longitudes_and_synodic_angles(start=start, end=end, bodies=bodies, step=step)

        # Fall back to original two-body behaviour
        if not body_1 or not body_2:
            raise ValueError("Either provide `bodies` (list) or both `body_1` and `body_2`")

        cache_file = f"{body_1}_{body_2}_{start}-{end}"
        cache_path = self.cache_dir / cache_file
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Cache load failed: {e}")

        dates = pd.date_range(start=start, end=end, freq=f'{step}D')
        if dates.empty:
            return pd.DataFrame()

        lon1 = self.get_heliocentric_longitudes_vectorized(dates, body_1)
        lon2 = self.get_heliocentric_longitudes_vectorized(dates, body_2)

        df = pd.DataFrame({
            body_1: lon1,
            body_2: lon2,
        }, index=dates)

        # Drop rows with NaN values
        df.dropna(inplace=True)
        if df.empty:
            return pd.DataFrame()

        # Vectorized angular separation calculation
        angle_diff = np.abs((df[body_2] - df[body_1]) % 360)
        df[f"{body_2}-{body_1}"] = np.minimum(angle_diff, 360 - angle_diff)

        # Cache the result
        try:
            logger.debug(f"Caching result for {body_1} and {body_2} from {start} to {end}")
            with open(cache_path, 'wb') as f:
                pickle.dump(df, f)
        except Exception as e:
            logger.warning(f"cache fail to save: {e}")

        return df