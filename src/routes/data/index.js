const express = require('express');
const router = express.Router();
const createError = require('http-errors');
const mysql = require('mysql');
const connection = require('../../lib/connection');
const query = require('../../lib/query');
// python scripts called in nodejs
const countRepetitions = require('../../lib/python_count_repetitions');
const uploadSingle = require('../../lib/python_upload_single');
const countLinks = require('../../lib/python_count_links');
const searchesByHour = require('../../lib/python_searches_by_hour');
const searchesByTime = require('../../lib/python_searches_by_time');
// python scripts called in nodejs
const dotenv = require('dotenv').config();

const config = require('../../config');
const dbConfig = config.mySqlConfig;
const auth0Config = config.auth0Config;

const checkSecured = require('../../lib/middleware.secured');

router.use(checkSecured(auth0Config));

router.get('/',  async (req, res, next) => {
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
});

router.post('/', (req, res, next) => {
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
});

router.get('/cntOrig', (req, res, next) => {
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
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
});

router.get('/cntDest', (req, res, next) => {
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
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
});

router.get('/origDestPairs', (req, res, next) => {

    const m = new Date();
    const dateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth()+1)).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(dateString);

    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString);

    // The data sent in the response is provided by a python script, check python_count_repetitions.js for more info
    // arg1: start date, inclusive (YYYY-MM-DD)
    // arg2: end date, inclusive (YYYY-MM-DD)
    // arg3: date type {'travel', 'request'}
    // arg4: most or least common stations {'top', 'bottom'}
    // arg5: integer for number of rows to include
    countLinks(
      req.arg1 || lastMonthDateString,
      req.arg2 || dateString,
      req.arg3 || 'travel',
      req.arg4 || 'top',
      req.arg5 || '10'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
});

router.get('/searchesByTime', (req, res, next) => {
    const m = new Date();
    const dateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth()+1)).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(dateString);

    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString);

    // The data sent in the response is provided by a python script, check python_searches_by_time.js for more info
    // arg1: start date, inclusive (YYYY-MM-DD)
    // arg2: end date, inclusive (YYYY-MM-DD)
    // arg3: date type {'travel', 'request'}
    // arg4: aggregate by day, month or year {'D', 'M', 'Y'}
    searchesByTime(
      req.arg1 || lastMonthDateString,
      req.arg2 || dateString,
      req.arg3 || 'travel',
      req.arg4 || 'D'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
});

router.get('/searchesByHour', (req, res, next) => {
    const m = new Date();
    const dateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth()+1)).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(dateString);

    const lastMonthDateString = m.getUTCFullYear() + "/" + ("0" + (m.getUTCMonth())).slice(-2) + "/" + ("0" + m.getUTCDate()).slice(-2);
    console.log(lastMonthDateString);

    // The data sent in the response is provided by a python script, check python_searches_by_hour.js for more info
    // arg1: start date, inclusive (YYYY-MM-DD)
    // arg2: end date, inclusive (YYYY-MM-DD)
    // arg3: date type {'travel', 'request'}
    searchesByHour(
      req.arg1 || lastMonthDateString,
      req.arg2 || dateString,
      req.arg3 || 'travel'
    ).then((data) => {
      console.log(data);
      res.send(data);
    }).catch((err) => {
      console.log(err);
      next(err);
    });
});


module.exports = router;
