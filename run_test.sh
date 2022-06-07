#!/bin/sh
sudo -u borjagonzalez dropdb capstonedb_test
sudo -u borjagonzalez createdb capstonedb_test
sudo -u borjagonzalez psql capstonedb_test < capstone.psql