require('dotenv').config();

module.exports = { user: process.env.USER,
   password: process.env.PASSWORD,
    host: process.env.HOST,
     database: process.env.DATABASE };
