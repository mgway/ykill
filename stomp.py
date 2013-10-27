#!/usr/bin/env python3

import atexit
import json
import time

import db
import importer
import log
import stomp

class KillListener:
	def on_message(self, headers, message):
		data = json.loads(message)
		with db.cursor() as c:
			print('inserting kill')
			importer.insert_kill(c, data)

	def on_error(self, headers, message):
		log.write('stomp error: {}, {}'.format(headers, message))
		log.flush()

conn = stomp.Connection([('stomp.zkillboard.com', 61613)])
conn.set_listener('', KillListener())
conn.start()
conn.connect()
conn.subscribe(destination='/topic/kills', id=1, ack='auto')

def exit():
	conn.disconnect()
	log.close()
atexit.register(exit)

while True:
	try:
		time.sleep(60)
	except KeyboardInterrupt:
		break
	log.flush()