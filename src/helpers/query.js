module.exports = (conn, q, params) => new Promise(
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
