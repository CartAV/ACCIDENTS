SELECT *
FROM accidents_pg_prep 
    LEFT JOIN LATERAL (
        SELECT "ID_RTE500",
               st_distance(geom_acc, the_geom) as distance_route_accident,
               st_ClosestPoint(the_geom::geometry, geom_acc::geometry) as projected_point
        FROM "public"."ign_troncon_route_postgis"
        WHERE st_dwithin(geom_acc, "the_geom", 100)
        ORDER BY distance_route_accident
        LIMIT 1
    ) as nearest_route
    ON true