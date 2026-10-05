# River and catchment spatial layer governance

This folder now registers the official Nepal river/catchment authority chain and the database design needed for spatial queries.

## Geometry model

- Hydropower project / station references: **Point**
- River / stream network: **LineString / MultiLineString**
- River basin / catchment / sub-catchment: **Polygon / MultiPolygon**
- Gauge / outlet / intake / dam / powerhouse: **Point** with an explicit facility-role field

## Coordinate rule

The public web/interchange geometry is normalized to **WGS 84 / EPSG:4326**. This is deliberate: GeoJSON and Leaflet use longitude/latitude, and one projected CRS is not appropriate for all of Nepal because the Survey Department national mapping system uses three 3-degree Transverse Mercator / Modified UTM zones centred at 81°E, 84°E and 87°E.

For PostGIS queries, keep `geom_wgs84` with a GiST index and also use `geography` for national-scale distances and areas. For local engineering calculations that require planar metres, transform to the verified Nepal TM/MUTM zone or another explicitly documented engineering CRS appropriate to the feature location.

## Authority boundary

The Survey Department's hydrographic vector layer is an official source, but the government distribution rules do not justify silently republishing the raw licensed geometry in this public GitHub repository. WECS officially defines the national river-basin framework. Their basin names and source metadata are registered here; polygon geometry remains pending until a governed redistributable vector extract is admitted.

This prevents the research website from presenting guessed river lines or hand-drawn basin polygons as official GIS data.
