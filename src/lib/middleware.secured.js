const jwt = require('express-jwt');
const jwks = require('jwks-rsa');

module.exports = (config) => (req, res, next) => {
  // Authentication middleware. When used, the
  // Access Token must exist and be verified against
  // the Auth0 JSON Web Key Set
  try {
    const jwtCheck = jwt({
      // Dynamically provide a signing key
      // based on the kid in the header and
      // the signing keys provided by the JWKS endpoint.
      secret: jwks.expressJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: `https://${config.AUTH0_DOMAIN}/.well-known/jwks.json`
      }),
      // Validate the audience and the issuer.
      audience: config.AUTH0_API_AUDIENCE,
      issuer: `https://${config.AUTH0_DOMAIN}/`,
      algorithms: ['RS256']
    });
    console.log('jwtCheck')
    next();
  } catch (err) {
    console.log(err);
    next(err);
  }
};
