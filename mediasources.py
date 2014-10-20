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
    lastProcessed_tag_sets_id = 0

    while not stopIteration:
        tagSets = mc.tagSetList(last_tag_sets_id=lastProcessed_tag_sets_id)
        if len(tagSets) == 0:
            stopIteration = True
        else:
            print "============================"
            print "More records: " + str(len(tagSets))
            print "============================"
            for tagSet in tagSets:
                print tagSet['name']
                cur.execute('INSERT INTO tag_set '
                            '(tag_sets_id, name, label, description, show_on_media, show_on_stories)'
                            'values (%s, %s, %s, %s, %s, %s)',
                            (tagSet['tag_sets_id'], tagSet['name'], tagSet['label'], tagSet['description'],
                            tagSet['show_on_media'], tagSet['show_on_stories']))
                lastProcessed_tag_sets_id = tagSet['tag_sets_id']

                stopNestedIteration = False
                lastProcessed_tags_id = 0
                while not stopNestedIteration:
                    tags = mc.tagList(tag_sets_id=tagSet['tag_sets_id'], last_tags_id=lastProcessed_tags_id)
                    if len(tags) == 0:
                        stopNestedIteration = True
                    else:
                        print "============================"
                        print "More records: " + str(len(tags))
                        print "============================"
                        for tag in tags:
                            print tag['tag']
                            cur.execute('INSERT INTO tag '
                                        '(tags_id, tag_sets_id, tag, label, description, show_on_media, show_on_stories)'
                                        'values (%s, %s, %s, %s, %s, %s, %s)',
                                        (tag['tags_id'], tag['tag_sets_id'], tag['tag'], tag['label'], tag['description'],
                                        tag['show_on_media'], tag['show_on_stories']))
                            lastProcessed_tags_id = tag['tags_id']

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

    stopIteration = False
    lastProcessed_media_id = 0

    while not stopIteration:
        media = mc.mediaList(lastProcessed_media_id, 50000)
        if len(media) == 0:
            stopIteration = True
        else:
            print "============================"
            print "More records: " + str(len(media))
            print "============================"
            for medium in media:
                print medium['url']
                lastProcessed_media_id = medium['media_id']
                if len(medium['url']) <= 500:
                    cur.execute('INSERT INTO media '
                                '(media_id, url, name)'
                                'values (%s, %s, %s)',
                                (medium['media_id'], medium['url'], medium['name']))
                    if 'media_sets' in medium.keys():
                        for media_set_aux in medium['media_sets']:
                            print '...' + str(media_set_aux['media_sets_id'])
                            cur.execute("INSERT into media_media_set "
                                        "(media_id, media_sets_id) "
                                        "values (%s, %s)",
                                        ( medium['media_id'], media_set_aux['media_sets_id']))
                    if 'media_source_tags' in medium.keys():
                        for tag_aux in medium['media_source_tags']:
                            print '...' + str(tag_aux['tags_id'])
                            cur.execute("INSERT into media_tag "
                                        "(media_id, tags_id) "
                                        "values (%s, %s)",
                                        ( medium['media_id'], tag_aux['tags_id']))