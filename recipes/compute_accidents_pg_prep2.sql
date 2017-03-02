SELECT *
FROM accidents_pg_prep, 
    LATERAL (SELECT "ID_RTE500", st_distance(geom_acc, the_geom) as distance_route_accident
     FROM "public"."ign_troncon_route_postgis"
     where st_dwithin(geom_acc, "the_geom", 50)
     ORDER BY distance_route_accident
    LIMIT 1) as nearest_route