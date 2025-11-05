"""
Veilborn - RPG Game with Machine Learning
"""

__version__ = "1.0.0"

from .player import Player
from .enemy import Enemy
from .asset_manager import AssetManager
from .ml_system import (
    BattleDifficultyClassifier,
    VictoryPredictor,
    WeaponRecommender,
    DifficultyAdjuster
)

__all__ = [
    'Player',
    'Enemy',
    'AssetManager',
    'BattleDifficultyClassifier',
    'VictoryPredictor',
    'WeaponRecommender',
    'DifficultyAdjuster'
]
