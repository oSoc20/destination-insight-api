var express = require('express');
var router = express.Router();
var passport = require('passport');

// load environment variables
var dotenv = require('dotenv');
dotenv.config();

var util = require('util');
var url = require('url');
var queryString = require('querystring');


// login and redirect to callback
router.get('/login', passport.authenticate('auth0', {
  scope: 'openid email profile'
}), (req, res) => {
  res.redirect('/api');
});

router.get('/callback', (req, res, next) => {
  passport.authenticate('auth0', (err, user, info) => {
    if (err) { return next(err); }
    if (!user) { return res.redirect('api/auth/login'); }

    req.logIn(user, (err) => {
      if (err) { return next(err); }
      const returnTo = req.session.returnTo;
      delete req.session.returnTo;
      res.redirect(returnTo || '/api');
    });
  }) (req, res, next);
});

// logout and redirect to homepage
router.get('/logout', (req, res) => {
  req.logout();

  let returnTo = req.protocol + '://' + req.hostname;
  const port = req.connection.localPort;
  if (port !== undefined && port !== 80 && port !== 443) {
    returnTo += ':' + port + '/api/';
  }
  console.log(returnTo);
  const logoutURL = new url.URL(
    util.format('https://%s/v2/logout', process.env.AUTH0_DOMAIN)
  );
  //console.log(logoutURL);
  const searchString = queryString.stringify({
    client_id: process.env.AUTH0_CLIENT_ID,
    returnTo: returnTo
  });
  logoutURL.search = searchString;

  res.redirect(logoutURL);
});

module.exports = router;
