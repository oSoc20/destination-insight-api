const express = require('express');
const router = express.Router();
const createError = require('http-errors');
const mysql = require('mysql');
const connection = require('../../utils/connection');
const query = require('../../utils/query');
// python scripts called in nodejs
const countRepetitions = require('../../utils/python_count_repetitions');
const uploadSingle = require('../../utils/python_upload_single');
const countLinks = require('../../utils/python_count_links');
const searchesByHour = require('../../utils/python_searches_by_hour');
const searchesByTime = require('../../utils/python_searches_by_time');
// python scripts called in nodejs
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
  .post('/', (req, res, next) => {
    const data = req.files.file;

    //place the file in the upload directory, just for the sake of organization
    const uploadPath = 'python_tools/uploads/';
    data.mv(uploadPath + data.name).then(() => {

      // this script will check if the file has already been uploaded, clean the data, and upload it
      // arg1: name of the directory that contains the file
      // arg2: name of the file to upload

      uploadSingle(data.name).catch((err) => {
        console.log(err);
        next(err);
      });
    }).then(() => {
      res.send({
        status: true,
        message: 'File uploaded',
        data: {
          name: data.name,
          mimetype: data.mimetype,
          size: data.size
        }
      });
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/cntOrig/:startDate?:endDate?:dateType?:topOrBottom?:rows?', (req, res, next) => {
    // sends a response with the top X origins searched
    // query arguments can be passed as
    // http://localhost:3000/api/data/cntOrig/?startDate=2000/01/01&endDate=2000/01/01

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    //  startDate: start date, inclusive (YYYY-MM-DD)
    //  endDate: end date, inclusive (YYYY-MM-DD)
    //  dateType: date type {'travel', 'request'}
    //  topOrBottom: most or least common stations {'top', 'bottom'}
    //  rows: integer for number of rows to include
    countRepetitions(
      'origin',
      req.query.startDate || '2000/01/01',
      req.query.endDate || '2050/01/01',
      req.query.dateType || 'travel',
      req.query.topOrBottom || 'top',
      req.query.rows || '10'
    ).then((data) => {
      console.log(data)
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/cntDest/:startDate?:endDate?:dateType?:topOrBottom?:rows?', (req, res, next) => {
    // sends a response with the top X destinations searched
    // query arguments can be passed as
    // http://localhost:3000/api/data/cntDest/?startDate=2000/01/01&endDate=2000/01/01

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    //  startDate: start date, inclusive (YYYY-MM-DD)
    //  endDate: end date, inclusive (YYYY-MM-DD)
    //  dateType: date type {'travel', 'request'}
    //  topOrBottom: most or least common stations {'top', 'bottom'}
    //  rows: integer for number of rows to include
    countRepetitions(
      'destination',
      req.query.startDate || '2000/01/01',
      req.query.endDate || '2050/01/01',
      req.query.dateType || 'travel',
      req.query.topOrBottom || 'top',
      req.query.rows || '10'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/origDestPairs/:startDate?:endDate?:dateType?:topOrBottom?:rows?', (req, res, next) => {
    // sends a response with the top X origin and destination pairs
    // query arguments can be passed as
    // http://localhost:3000/api/data/origDestPairs/?startDate=2000/01/01&endDate=2000/01/01

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    // startDate: start date, inclusive (YYYY-MM-DD)
    // endDate: end date, inclusive (YYYY-MM-DD)
    // dateType: date type {'travel', 'request'}
    // topOrBottom: most or least common stations {'top', 'bottom'}
    // rows: integer for number of rows to include
    countLinks(
      req.query.startDate || '2000/01/01',
      req.query.endDate || '2050/01/01',
      req.query.dateType || 'travel',
      req.query.topOrBottom || 'top',
      req.query.rows || '10'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/searchesByTime/:startDate?:endDate?:dateType?:dayMonthOrYear?', (req, res, next) => {
    // sends a response with the number of searches by time
    // query arguments can be passed as
    // http://localhost:3000/api/data/searchesByTime/?startDate=2000/01/01&endDate=2000/01/01

    // The data sent in the response is provided by a python script, check python_searches_by_time.js for more info
    // startDate: start date, inclusive (YYYY-MM-DD)
    // endDate: end date, inclusive (YYYY-MM-DD)
    // dateType: date type {'travel', 'request'}
    // dayMonthOrYear: aggregate by day, month or year {'D', 'M', 'Y'}
    searchesByTime(
      req.query.startDate || '2000/01/01',
      req.query.endDate || '2050/01/01',
      req.query.dateType || 'travel',
      req.query.dayMonthOrYear || 'D'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  })
  .get('/searchesByHour/:startDate?:endDate?:dateType?', (req, res, next) => {
    // sends a response with the number of searches by hour
    // query arguments can be passed as
    // http://localhost:3000/api/data/searchesByHour/?startDate=2000/01/01&endDate=2000/01/01

    // The data sent in the response is provided by a python script, check python_searches_by_hour.js for more info
    // startDate: start date, inclusive (YYYY-MM-DD)
    // endDate: end date, inclusive (YYYY-MM-DD)
    // dateType: date type {'travel', 'request'}
    searchesByHour(
      req.query.startDate || '2000/01/01',
      req.query.endDate || '2050/01/01',
      req.query.dateType || 'travel'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
  });
