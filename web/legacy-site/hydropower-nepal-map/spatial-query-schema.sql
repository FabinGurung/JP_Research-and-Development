-- Hydropower PhD research spatial schema
-- Public-safe design reference for PostGIS implementation.
-- Canonical web/interchange geometry: EPSG:4326.
-- Metric work: geography or a verified projected CRS appropriate to the feature location.

create table if not exists spatial_source (
  source_id text primary key,
  provider text not null,
  dataset_name text not null,
  source_url text not null,
  source_crs text,
  licence_or_distribution_rule text,
  redistribution_allowed boolean,
  authority_status text not null,
  notes text
);

create table if not exists river_feature (
  river_id text primary key,
  river_name text,
  alternate_names text[],
  basin_id text,
  stream_order integer,
  source_id text not null references spatial_source(source_id),
  source_feature_id text,
  source_crs text,
  geom_wgs84 geometry(MultiLineString,4326),
  geog geography(MultiLineString,4326),
  transformation_method text,
  provenance_note text
);

create index if not exists river_feature_geom_gix on river_feature using gist (geom_wgs84);
create index if not exists river_feature_geog_gix on river_feature using gist (geog);

create table if not exists catchment_feature (
  catchment_id text primary key,
  catchment_name text not null,
  catchment_level text not null,
  parent_catchment_id text references catchment_feature(catchment_id),
  outlet_river_id text references river_feature(river_id),
  source_id text not null references spatial_source(source_id),
  source_feature_id text,
  source_crs text,
  geom_wgs84 geometry(MultiPolygon,4326),
  geog geography(MultiPolygon,4326),
  transformation_method text,
  provenance_note text
);

create index if not exists catchment_feature_geom_gix on catchment_feature using gist (geom_wgs84);
create index if not exists catchment_feature_geog_gix on catchment_feature using gist (geog);

-- Existing hydropower projects can reference the spatial fabric without copying names.
create table if not exists hydropower_spatial_link (
  project_id text not null,
  catchment_id text references catchment_feature(catchment_id),
  nearest_river_id text references river_feature(river_id),
  link_method text not null,
  link_distance_m double precision,
  source_or_run_id text not null,
  primary key (project_id, source_or_run_id)
);

-- Example query patterns:
-- 1) Projects inside a catchment:
--    ST_Contains(c.geom_wgs84, p.geom_wgs84)
-- 2) Rivers crossing a catchment:
--    ST_Intersects(r.geom_wgs84, c.geom_wgs84)
-- 3) Distance from project to river, spheroidal metres:
--    ST_Distance(p.geog, r.geog)
-- 4) Catchment area, spheroidal square metres:
--    ST_Area(c.geog)
-- 5) Local engineering buffers/lengths:
--    ST_Transform(..., verified_projected_srid) only after the CRS is documented.
