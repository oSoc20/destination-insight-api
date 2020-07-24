const express = require('express');
const bodyParser = require('body-parser');
const createError = require('http-errors');
const routes = require('./routes');
const cors = require('cors');

// load environment variables
const dotenv = require('dotenv');
dotenv.config();

// simple express middleware for uploading files. It parses multipart/form-data requests
// extracts the files if available and makes them available under req.files property
const fileUpload = require('express-fileupload');

const app = express();
const port = 3000;

// enable file upload
app.use(fileUpload({
  preserveExtension: true
}));
// bodyparser parses the request body and transforms it into a js object for easy operation
app.use(bodyParser.json({}));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(cors({origin: "*"}));

// router
app.use('/api', routes);

// catch 404 and forward to error handler
app.use((req, res, next) => {
  next(createError(404));
});

//error handler
app.use((err, req, res, next) => {
  res.status(err.status || 500);
  res.json(err.message);
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`http://localhost:${port}/`);
});

module.exports = app;
