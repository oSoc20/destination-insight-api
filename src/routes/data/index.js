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

    const m = new Date();
    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString)

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
  .post('/', (req, res, next) => {
    try
    {
      const data = req.files.file;

      //place the file in the upload directory, just for the sake of organization
      data.mv('./src/python_tools/uploads/' + data.name);

      res.send({
        status: true,
        message: 'File uploaded',
        data: {
          name: data.name,
          mimetype: data.mimetype,
          size: data.size
        }
      })
    }
    catch (err) {
      console.log(err);
      next(err);
    };

  })
  .get('/cntOrig', (req, res, next) => {
    // sends a response with the top X origins searched

    const m = new Date();
    const dateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth()+1)).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(dateString);

    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString);

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    //  arg1: station type {'origin', 'destination'}
    //  arg2: start date, inclusive (YYYY-MM-DD)
    //  arg3: end date, inclusive (YYYY-MM-DD)
    //  arg4: date type {'travel', 'request'}
    //  arg5: most or least common stations {'top', 'bottom'}
    //  arg6: integer for number of rows to include
    countRepetitions(
      'origin',
      req.arg2 || lastMonthDateString,
      req.arg3 || dateString,
      req.arg4 || 'travel',
      req.arg5 || 'top',
      req.arg6 || '10'
    ).then((data) => {
      console.log(data)
      res.json(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/cntDest', (req, res, next) => {
    // sends a response with the top X destinations searched

    const m = new Date();
    const dateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth()+1)).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(dateString);

    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString);

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    //  arg1: station type {'origin', 'destination'}
    //  arg2: start date, inclusive (YYYY-MM-DD)
    //  arg3: end date, inclusive (YYYY-MM-DD)
    //  arg4: date type {'travel', 'request'}
    //  arg5: most or least common stations {'top', 'bottom'}
    //  arg6: integer for number of rows to include
    countRepetitions(
      'destination',
      req.arg2 || lastMonthDateString,
      req.arg3 || dateString,
      req.arg4 || 'travel',
      req.arg5 || 'top',
      req.arg6 || '10'
    ).then((data) => {
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
