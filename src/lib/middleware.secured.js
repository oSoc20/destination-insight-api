const jwt = require('express-jwt');
const jwks = require('jwks-rsa');

module.exports = (config) => (req, res, next) => {
  // Authentication middleware
  try {
    const jwtCheck = jwt({
      secret: jwks.expressJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: `https://${config.AUTH0_DOMAIN}/.well-known/jwks.json`
      }),
      audience: config.AUTH0_API_AUDIENCE,
      issuer: `https://${config.AUTH0_DOMAIN}/`,
      algorithms: ['RS256']
    });
    next();
  } catch (err) {
    console.log(err);
    next(err);
  }
};
