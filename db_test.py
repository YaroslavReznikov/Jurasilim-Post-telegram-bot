from parsing import Database_connector
import time


g = Database_connector()
g.database.commit()
g.database.close()