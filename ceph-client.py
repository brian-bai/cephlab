import rados

try:
        cluster = rados.Rados(conffile='')
except TypeError as e:
        print('Argument validation error: {}'.format(e))
        raise e

print("Created cluster handle.")

try:
        cluster.connect()
except Exception as e:
        print("connection error: {}".format(e))
        raise e
finally:
        print("Connected to the cluster.")