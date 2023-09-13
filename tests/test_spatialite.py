"""
Tests for functionalities in ogr_util.
"""

import pytest
import shapely.geometry as sh_geom

import geofileops as gfo
from tests import test_helper


@pytest.mark.skipif(
    not test_helper.RUNS_LOCAL,
    reason="Don't this run on CI: just to document this behaviour.",
)
def test_st_difference_null(tmp_path):
    """
    ST_difference returns NULL when 2nd argument is NULL.

    This is the normal treatment of NULL values: `SELECT (1-NULL)` also results in NULL.

    In several spatial operations IIF statements are used to handle this situation.
    """
    input_path = test_helper.get_testfile(testfile="polygon-parcel")

    sql_stmt = """
        SELECT *
          FROM "{input_layer}"
         WHERE ST_difference({geometrycolumn}, NULL) IS NULL
    """
    output_path = tmp_path / "output.gpkg"
    gfo.select(input_path, output_path, sql_stmt=sql_stmt)

    input_gdf = gfo.read_file(input_path)
    output_gdf = gfo.read_file(output_path)
    assert len(input_gdf) == len(output_gdf)


@pytest.mark.skipif(
    not test_helper.RUNS_LOCAL,
    reason="Don't this run on CI: just to document this behaviour.",
)
@pytest.mark.parametrize("ogr_type", ["WKB", "WKT"])
def test_nested_collections(ogr_type):
    """
    ST_difference returns NULL when 2nd argument is NULL.

    This is the normal treatment of NULL values: `SELECT (1-NULL)` also results in NULL.

    In several spatial operations IIF statements are used to handle this situation.
    """
    # Prepare test data
    input_path = test_helper.get_testfile(testfile="polygon-parcel")
    collection = sh_geom.GeometryCollection(
        [test_helper.TestData.multipolygon, test_helper.TestData.polygon_no_islands]
    )

    # Test
    if ogr_type == "WKB":
        sql_stmt = f"SELECT ST_GeomFromText('{collection.wkt}')"
    elif ogr_type == "WKT":
        sql_stmt = f"SELECT ST_GeomFromWKB(x'{collection.wkb_hex}')"

    test_gdf = gfo.read_file(input_path, sql_stmt=sql_stmt)
    assert test_gdf.geometry[0].wkt == collection.wkt
