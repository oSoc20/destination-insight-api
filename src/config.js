require('dotenv').config();

exports.auth0Config = {
  // example of params for auth0: {
  // AUTH0_DOMAIN: kmaida.auth0.com,
  // AUTH0_API_AUDIENCE: 'http://localhost:3000/api/'
  // }
   AUTH0_DOMAIN: process.env.AUTH0_DOMAIN,
   AUTH0_API_AUDIENCE: process.env.AUTH0_API_AUDIENCE
};

exports.mySqlConfig = {
  // params for mysql db are: {host, user, password, databate}
  SQL_HOST: process.env.SQL_HOST,
  SQL_USER: process.env.SQL_USERNAME,
  SQL_PASSWORD: process.env.SQL_PASSWORD,
  SQL_DATABASE: process.env.SQL_DATABASE
};
