######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
######################################################################

"""
Test cases for Product Model
"""

import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertIsNone(product.id)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertTrue(product.available)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a product from the database"""
        product = ProductFactory()
        product.create()
        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, product.name)

    def test_update_a_product(self):
        """It should Update a product in the database"""
        product = ProductFactory()
        product.create()
        product.name = "Updated Name"
        product.update()
        updated = Product.find(product.id)
        self.assertEqual(updated.name, "Updated Name")

    def test_delete_a_product(self):
        """It should Delete a product from the database"""
        product = ProductFactory()
        product.create()
        product_id = product.id
        product.delete()
        deleted = Product.find(product_id)
        self.assertIsNone(deleted)

    def test_list_all_products(self):
        """It should List all products"""
        ProductFactory().create()
        ProductFactory().create()
        products = Product.all()
        self.assertEqual(len(products), 2)

    def test_find_by_name(self):
        """It should Find products by name"""
        product = ProductFactory(name="Laptop")
        product.create()
        results = Product.find_by_name("Laptop").all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Laptop")

    def test_find_by_category(self):
        """It should Find products by category"""
        product = ProductFactory(category=Category.ELECTRONICS)
        product.create()
        results = Product.find_by_category(Category.ELECTRONICS).all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, Category.ELECTRONICS)

    def test_find_by_availability(self):
        """It should Find products by availability"""
        product = ProductFactory(available=True)
        product.create()
        results = Product.find_by_availability(True).all()
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].available)