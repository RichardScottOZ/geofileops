from packaging import version

import shapely

from geofileops.util import _sqlite_util

SHAPELY_GE_20 = version.parse(shapely.__version__) >= version.parse("2")

# Check what version of spatialite we are dealing with
spatialite_version_info = _sqlite_util.spatialite_version_info()
spatialite_version = spatialite_version_info["spatialite_version"]
SPATIALITE_GTE_51 = version.parse(spatialite_version) >= version.parse("5.1")
