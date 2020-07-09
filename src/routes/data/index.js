const express = require('express');
const router = express.Router();
const createError = require('http-errors');
const mysql = require('mysql');
const connection = require('../../helpers/connection');
const query = require('../../helpers/query');
const countRepetitions = require('../../helpers/python_count_repetitions');
const dotenv = require('dotenv').config();

const dbConfig = require('../../dbConfig');

module.exports = router

  .get('/', async (req, res, next) => {
    const conn = await connection(dbConfig)
      .catch((err) => {
        console.log(err);
        next(err);
      });
    const results = await query(conn, "SELECT * FROM searches")
      .catch((err) => {
        console.log(err);
        next(err);
      });
      res.json(results);
})
  .get('/repetitions', (req, res, next) => {
    // const result = countRepetitions;
    // res.json(result);
    countRepetitions().then((data) => {
      console.log(data)
      res.json(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
