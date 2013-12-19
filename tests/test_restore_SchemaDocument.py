# -*- coding: utf-8 -*-

#==============================================
#Created on Dec 11, 2013
#
#@author: Bertrand Néron
#@contact: bneron@pasteur.fr
#@organization: Institut Pasteur
#==============================================


import unittest

from mongokit import *

class RestoreSchemaDocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = Connection()
        self.col = self.connection['test']['mongokit']

    def tearDown(self):
        self.connection.drop_database('test')

    def test_restore_SD(self):
        class Pet(SchemaDocument):
            structure = {'name' : basestring }

        @self.connection.register
        class Canary(Pet):

            def say_hi(self):
                print "I tawt I taw a puddy tat!"

        @self.connection.register
        class Cat(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "Sufferin' succotash"

        class Dog(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "ouaf ouaf"

        @self.connection.register
        class GrandMa(Document):
            __database__ = 'test'
            __collection__ = 'granny'
            structure = {
                     '_type' : unicode,
                     'bird' : Canary,
                     'cat' : Cat,
                     'dog' : Dog,
                     'pets' : [Pet]
                     }
        tweety = Canary()
        tweety['name'] = 'Tweety'

        sylvester = Cat()
        sylvester['name'] = 'Sylvester'
        sylvester['catch'] = tweety

        hector = Dog()
        hector['name'] = 'Spike'
        hector['catch'] = sylvester

        granny= self.connection.GrandMa()
        granny['bird'] = tweety
        granny['cat'] = sylvester
        granny['dog'] = hector
        granny.save()
        meme_reloaded = self.connection.GrandMa.fetch_one({})
        self.assertEqual(type(meme_reloaded['bird']), type(tweety))
        self.assertEqual(meme_reloaded['bird']['name'], 'Tweety')
        self.assertEqual(type(meme_reloaded['cat']), type(sylvester))
        self.assertEqual(meme_reloaded['cat']['name'], 'Sylvester')
        self.assertEqual(type(meme_reloaded['dog']), type({}))
        self.assertEqual(meme_reloaded['dog']['name'], 'Spike')

    def test_restore_SD_in_list(self):
        class Pet(SchemaDocument):
            structure = {'name' : basestring }

        @self.connection.register
        class Canary(Pet):

            def say_hi(self):
                print "I tawt I taw a puddy tat!"

        @self.connection.register
        class Cat(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "Sufferin' succotash"

        class Dog(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "ouaf ouaf"

        @self.connection.register
        class GrandMa(Document):
            __database__ = 'test'
            __collection__ = 'granny'
            structure = {
                     '_type' : unicode,
                     'bird' : Canary,
                     'cat' : Cat,
                     'dog' : Dog,
                     'pets' : [Pet]
                     }
        tweety = Canary()
        tweety['name'] = 'Tweety'

        sylvester = Cat()
        sylvester['name'] = 'Sylvester'
        sylvester['catch'] = tweety

        hector = Dog()
        hector['name'] = 'Spike'
        hector['catch'] = sylvester

        granny= self.connection.GrandMa()
        granny['pets'] = [tweety, sylvester , hector]
        granny.save()
        meme_reloaded = self.connection.GrandMa.fetch_one({})
        self.assertEqual(type(meme_reloaded['pets']), type([]))
        self.assertEqual(type(meme_reloaded['pets'][0]), type(tweety))
        self.assertEqual(type(meme_reloaded['pets'][1]), type(sylvester))
        self.assertEqual(type(meme_reloaded['pets'][2]), type({}))


    def test_restore_recursive_SD(self):
        class Pet(SchemaDocument):
            structure = {'name' : basestring }

        @self.connection.register
        class Canary(Pet):

            def say_hi(self):
                print "I tawt I taw a puddy tat!"

        @self.connection.register
        class Cat(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "Sufferin' succotash"

        class Dog(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "ouaf ouaf"

        @self.connection.register
        class GrandMa(Document):
            __database__ = 'test'
            __collection__ = 'granny'
            structure = {
                     '_type' : unicode,
                     'bird' : Canary,
                     'cat' : Cat,
                     'dog' : Dog,
                     'pets' : [Pet]
                     }
        tweety = Canary()
        tweety['name'] = 'Tweety'

        sylvester = Cat()
        sylvester['name'] = 'Sylvester'
        sylvester['catch'] = tweety

        hector = Dog()
        hector['name'] = 'Spike'
        hector['catch'] = sylvester

        granny= self.connection.GrandMa()
        granny['bird'] = tweety
        granny['cat'] = sylvester
        granny['dog'] = hector
        granny['pets'] = [tweety, sylvester , hector]
        granny.save()
        meme_reloaded = self.connection.GrandMa.fetch_one({})
        sylvester_2 = meme_reloaded['cat']
        self.assertEqual(type(sylvester_2['catch']), type(tweety))
        self.assertEqual(sylvester_2['catch']['name'], 'Tweety')
        hector_2 = meme_reloaded['dog']
        self.assertEqual(type(hector_2['catch']), type(sylvester))
        self.assertEqual(hector_2['catch']['name'], 'Sylvester')

    def test_restore_in_dict(self):
        class Pet(SchemaDocument):
            structure = {'name': basestring }

        @self.connection.register
        class Canary(Pet):

            def say_hi(self):
                print "I tawt I taw a puddy tat!"

        @self.connection.register
        class Cat(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "Sufferin' succotash"

        class Dog(Pet):
            structure = {
                         'catch': Pet
                         }

            def say_hi(self):
                print "ouaf ouaf"

        @self.connection.register
        class GrandMa(Document):
            __database__ = 'test'
            __collection__ = 'granny'
            structure = {
                     '_type': unicode,
                     'pets': {unicode: Pet}
                     }

        tweety = Canary()
        tweety['name'] = 'Tweety'

        sylvester = Cat()
        sylvester['name'] = 'Sylvester'

        hector = Dog()
        hector['name'] = 'Spike'

        granny = self.connection.GrandMa()
        granny['pets'] = {u'tweety': tweety,
                          u'sylvester': sylvester,
                          u'hector': hector}
        granny.save()
        meme_reloaded = self.connection.GrandMa.fetch_one({})
        tweety_2 = meme_reloaded['pets'][u'tweety']
        sylvester_2 = meme_reloaded['pets'][u'sylvester']
        hector_2 = meme_reloaded['pets'][u'hector']
        self.assertIs(type(tweety_2), Canary)
        self.assertIs(type(sylvester_2), Cat)
        self.assertIs(type(hector_2), type({}))
