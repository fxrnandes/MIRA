"""Testes unitários para world/grid.py — execute com: pytest tests/ -v"""
import pytest
from world.grid import Grid
from world.cell import CellType


class TestGridInitialization:
    def test_grid_stores_width(self):
        assert Grid(10, 5).width == 10

    def test_grid_stores_height(self):
        assert Grid(10, 5).height == 5

    def test_grid_cells_default_to_free(self):
        grid = Grid(3, 3)
        for row in grid._cells:
            assert all(c == CellType.FREE for c in row)


class TestGridAccess:
    def test_get_cell_returns_free_by_default(self):
        grid = Grid(5, 5)
        assert grid.get_cell(2, 2) == CellType.FREE

    def test_set_and_get_cell(self):
        grid = Grid(5, 5)
        grid.set_cell(1, 1, CellType.WALL)
        assert grid.get_cell(1, 1) == CellType.WALL

    def test_set_fire_cell(self):
        grid = Grid(5, 5)
        grid.set_cell(3, 3, CellType.FIRE)
        assert grid.get_cell(3, 3) == CellType.FIRE


class TestGridNeighbors:
    def test_center_has_four_neighbors(self):
        grid = Grid(5, 5)
        assert len(grid.neighbors(2, 2)) == 4

    def test_corner_has_two_neighbors(self):
        grid = Grid(5, 5)
        assert len(grid.neighbors(0, 0)) == 2

    def test_edge_has_three_neighbors(self):
        grid = Grid(5, 5)
        assert len(grid.neighbors(0, 2)) == 3


class TestGridWalkable:
    def test_free_cell_is_walkable(self):
        grid = Grid(5, 5)
        assert grid.is_walkable(2, 2) is True

    def test_wall_is_not_walkable(self):
        grid = Grid(5, 5)
        grid.set_cell(1, 1, CellType.WALL)
        assert grid.is_walkable(1, 1) is False

    def test_fire_is_not_walkable(self):
        grid = Grid(5, 5)
        grid.set_cell(2, 2, CellType.FIRE)
        assert grid.is_walkable(2, 2) is False

    def test_exit_is_walkable(self):
        grid = Grid(5, 5)
        grid.set_cell(4, 4, CellType.EXIT)
        assert grid.is_walkable(4, 4) is True
