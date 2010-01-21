SELECT * INTO OUTFILE '/tmp/doorstep.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM tourist;

SELECT md5, CONCAT(lat, ",", lng), title, description, href, picture, CONCAT(region, ", ", country), free, modified INTO OUTFILE '/tmp/10.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM place LIMIT 10;
