const mysql = require('mysql');

module.exports = async (params) => new Promise(
  (resolve, reject) => {
    // params are: {host, user, password, databate} we have them in a .env file
    // these values are stocked in dbConfig.js
      const connection = mysql.createConnection(params);
    connection.connect(err => {
      if (err) {
        reject(err);
        return;
      }
      resolve(connection);
    })
  }
);
