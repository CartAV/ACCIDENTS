SELECT *
  FROM "accidents_pg_prep"

SELECT *, "ID_RTE500", distance_route_accident
FROM accidents_pg_prep, 
    LATERAL (SELECT "ID_RTE500", st_distance(geom_acc, the_geom) as dist
     FROM "public"."ign_troncon_route_postgis"
     where geom_acc && "the_geom"
     ORDER BY dist
    LIMIT 1) as nearest_route