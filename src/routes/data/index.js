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
    // Establish a connection with the mySQL database, check connection.js for more info
    const conn = await connection(dbConfig)
      .catch((err) => {
        console.log(err);
        next(err);
      });
      // Run an SQL query, check query.js for more info
    const results = await query(conn, "SELECT * FROM searches")
      .catch((err) => {
        console.log(err);
        next(err);
      });
      res.json(results);
})
  .get('/repetitions', (req, res, next) => {
    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    countRepetitions().then((data) => {
      console.log(data)
      res.json(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/commonArrivalDestination', (req, res, next) => {
    // call python script from here
  })
  .get('/mostSearched', (req, res, next) => {
    // call python script from here
  })
  .get('/findBetweenDates', (req, res, next) => {
    // call python script from here
  })
  .get('/requestAndTravelTimes', (req, res, next) => {
    // call python script from here
  })
  .get('/requestByHour', (req, res, next) => {
    // call python script from here
  })
  .get('/requestByDay', (req, res, next) => {
    // call python script from here
  })
  .get('/searchesByLanguage', (req, res, next) => {
    // call python script from here
  });
