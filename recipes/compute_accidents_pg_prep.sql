SELECT *,
  st_setSRID(st_makepoint(longitude, latitude), 4326) as geom_acc
  FROM "accidents_pg"