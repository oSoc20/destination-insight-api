// here we will use the connection we establish in connection.js
// to run an SQL query
module.exports = async (conn, q, params) => new Promise(
  (resolve, reject) => {
    const handler = (err, result) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(result);
    }
    conn.query(q, params, handler);
});
