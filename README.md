# Great-circle distance
MySQL vs PostgreSQL benchmarks

## setup
PostgreSQL requires the `earthdistance` package.

```sql
create extension cube;
create extension earthdistance;
```

Make sure your MySQL server instance contains a `geo` table.

```sh
# Generate and fill database tables necessary for benchmarks
make

# Run benchmarks
./mysql.sh
./postgres.sh
```

## select statements
```sql
-- MySQL
SELECT (6378.137 * acos(cos(radians(ST_X(p1))) * cos(radians(ST_X(p2))) * cos(radians(ST_Y(p2)) - radians(ST_Y(p1))) + sin(radians(ST_X(p1))) * sin(radians(ST_X(p2))))) AS distance
-- vs PostgreSQL
SELECT (p1 <@> p2) * 1.609344 AS distance
```

## results
coming soon
