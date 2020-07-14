require('dotenv').config();

module.exports = { user: process.env.USER || 'localhost',
   password: process.env.PASSWORD || 'root',
    host: process.env.HOST || '',
     database: process.env.DATABASE || 'test' };
