SELECT *, "ID_RTE500", distance_route_accident
FROM accidents_pg_prep, 
    LATERAL (SELECT "ID_RTE500", st_distance(geom_acc, the_geom) as distance_route_accident
     FROM "public"."ign_troncon_route_postgis"
     where geom_acc && "the_geom"
     ORDER BY distance_route_accident
    LIMIT 1) as nearest_route