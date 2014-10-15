# -*- coding: utf-8 -*-
import mediacloud
import ConfigParser
import MySQLdb as myDB

config = ConfigParser.ConfigParser()
config.read('info.config')

mc = mediacloud.api.MediaCloud(config.get('api','key'))
con = myDB.connect(config.get('db','host'), config.get('db','username'),
                   config.get('db','password'), config.get('db','schema'))

with con:
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    stopIteration = False
    lastProcessed_media_sets_id = 0

    while not stopIteration:
        mediaSets = mc.mediaSetList(lastProcessed_media_sets_id)
        if len(mediaSets) == 0:
            stopIteration = True
        else:
            print "============================"
            print "More records: " + str(len(mediaSets))
            print "============================"
            for mediaSet in mediaSets:
                print mediaSet['name']
                cur.execute('INSERT INTO media_set '
                            '(media_sets_id, name, description)'
                            'values (%s, %s, %s)',
                            (mediaSet['media_sets_id'], mediaSet['name'], mediaSet['description']))
                lastProcessed_media_sets_id = mediaSet['media_sets_id']