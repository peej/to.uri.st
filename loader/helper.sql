SELECT * INTO OUTFILE '/tmp/doorstep.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM tourist;

SELECT md5, CONCAT(lat, ",", lng), title, description, href, picture, CONCAT(region, ", ", country), free, modified, type INTO OUTFILE '/tmp/attractions.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM place;

select round(lat,2), round(lng,2), group_concat(md5) INTO OUTFILE '/tmp/geobox.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' from place group by round(lat, 2), round(lng, 2);


~/google_appengine/appcfg.py upload_data --config_file=loader/attraction.py --filename=/tmp/attractions.csv --kind=Attraction --url=http://localhost:8080/remote_api .

~/google_appengine/appcfg.py upload_data --config_file=loader/geobox.py --filename=/tmp/geobox.csv --kind=GeoBox --url=http://localhost:8080/remote_api .


SELECT md5, CONCAT(lat, ",", lng), title, description, href, picture, CONCAT(region, ", ", country), free, modified, type INTO OUTFILE '/tmp/attractions.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM place WHERE lng > 0 AND lng < 1;

select round(lat,1), round(lng,1), group_concat(md5) INTO OUTFILE '/tmp/geobox.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' from place WHERE lng > 0 AND lng < 1 group by round(lat, 1), round(lng, 1);
