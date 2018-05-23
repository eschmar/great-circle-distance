import sys, random, subprocess

OUTPUT_FOLDER = "./build"

areas = {
    'goteborg': [11.557617187499998, 57.97315745102812, 12.94189453125, 57.33838126552897],
    'malmo': [12.821044921875, 55.86298231197633, 13.7109375, 55.34164183013326],
    'stockholm': [16.995849609375, 59.92199002450385, 19.31396484375, 58.859223547066584],
    'umea': [18.4130859375, 64.24936824742616, 20.665283203125, 63.44559823038747]
}

def parseArguments(argv):
    """Parses cli input -options and --flags into a dictionary."""
    params = {}
    points = []
    while argv:
        if argv[0][0] == '-' and argv[0][1] == '-':
            # Found flag
            params[argv[0]] = True
        elif argv[0][0] == '-' and argv[0][1] == 'x':
            # Found individual
            points.append(argv[1])
        elif argv[0][0] == '-':
            # Found option
            params[argv[0]] = argv[1]
        argv = argv[1:]

    params['-x'] = points
    return params

def getRandomCoords():
    rkey = random.choice(list(areas))
    rx = random.uniform(areas[rkey][0], areas[rkey][2])
    ry = random.uniform(areas[rkey][1], areas[rkey][3])
    return rx, ry, rkey

def run(args):
    params = parseArguments(args)

    # default values
    seed = 4096
    sampleSize = 10000
    database = "temp"
    databasetype = "mysql"

    # check size for user input
    if '-N' in params:
        val = int(params['-N'])
        if val < 1:
            raise ValueError("Sample size has to be positive.")
        sampleSize = val
    
    # check seed for user input
    if '-S' in params:
        val = int(params['-S'])
        if val < 1:
            raise ValueError("Seed has to be positive.")
        seed = val

    # check seed for user input
    if '-D' in params:
        database = params['-D']
    
    if '-T' in params:
        if params['-T'] != "mysql" and params['-T'] != "postgres":
            raise ValueError("Database -T [mysql|postgres].")
        databasetype = params['-T']


    random.seed(seed)

    chunks=500
    if sampleSize < 500:
        chunks = 100
    
    table = "geo_" + str(sampleSize)

    # Output
    with open(OUTPUT_FOLDER + '/mysql.sql', 'w') as mysql, open(OUTPUT_FOLDER + '/postgres.sql', 'w') as postgres:
        #  MYSQL
        mysql.write('DROP TABLE IF EXISTS `' + table + '`;\n')
        mysql.write('CREATE TABLE `' + table + '` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT, `p1` point DEFAULT NULL, `p2` point DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n')
        mysql.write('TRUNCATE TABLE `' + table + '`;\n\n')


        # POSTGRES
        postgres.write('DROP TABLE IF EXISTS `' + table + '`;\n')
        postgres.write('CREATE TABLE "' + table + '" ("id" SERIAL, "p1" point, "p2" point, PRIMARY KEY ("id"));\n')
        postgres.write('TRUNCATE TABLE `' + table + '`;\n\n')

        for j in range(0, int(sampleSize / chunks)):
            mvalues = ''
            pvalues = ''

            for i in range(0, chunks):
                x, y, key = getRandomCoords()
                x2, y2, key2 = getRandomCoords()
                mvalues += " (GeomFromText(\'POINT(%s %s)\'), GeomFromText(\'POINT(%s %s)\'))" % (str(x), str(y), str(x2), str(y2))
                pvalues += " ((%s,%s), (%s,%s))" % (str(x), str(y), str(x2), str(y2))
                if i < chunks - 1:
                    mvalues += ','
                    pvalues += ','
            
            mysql.write("INSERT INTO %s (p1, p2) VALUES%s;\n" % (table, mvalues))
            postgres.write("INSERT INTO %s (p1, p2) VALUES%s;\n" % (table, pvalues))

if __name__ == '__main__':
    run(sys.argv[1:])
