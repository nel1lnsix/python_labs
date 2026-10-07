"""Сборник функций из лабораторных работ (реэкспорт, собственного кода нет)."""
import os
import sys

# чтобы импорт работал и при запуске файла напрямую из папки lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab02.arrays import min_max, unique_sorted, flatten
from lab02.matrix import transpose, row_sums, col_sums
from lab02.tuples import format_record
