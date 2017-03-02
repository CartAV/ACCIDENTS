SELECT *,
  st_setSRID(st_makepoint(longitude, latitude), 4326)::geography(Point) as geom_acc
  FROM "accidents_pg"