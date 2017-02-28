SELECT *
  st_setSRID(st_makepoint(longitude, latitude), 4326) as geom_accident
  FROM "caracteristiques_prep_geo_joined"