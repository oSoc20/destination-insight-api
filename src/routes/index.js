const express = require('express');
const router = express.Router();
const createError = require('http-errors');
const dataRoutes = require('./data');
const authRoutes = require('./auth');

router.get('/', (req, res, next) => {
  res.send('Server works!');
});

router.use('/data', dataRoutes);
router.use('/auth', authRoutes);

module.exports = router;
