
module.exports = (arg1, arg2, arg3, arg4, arg5, arg6) => new Promise((resolve, reject) => {
  const spawn = require('child_process').spawn;

  // spawn(command, [arg1, args], {options})
  // spawn(<string>, string[], Object)
  // arg1 is the script we want to run
  // args are aditional arguments all separated by a ","
  // options is, well, aditional options

  //  this script will return a json table with the top or bottom stations by number of searches in origin or destination
  //  arg1: station type {'origin', 'destination'}
  //  arg2: start date, inclusive (YYYY-MM-DD)
  //  arg3: end date, inclusive (YYYY-MM-DD)
  //  arg4: date type {'travel', 'request'}
  //  arg5: most or least common stations {'top', 'bottom'}
  //  arg6: integer for number of rows to include

  //  command example: python count_repetitions.py origin 2020-05-13 2020-05-14 travel top 10

  // call the python script from the script's directory (cwd)
  const pythonScript = spawn('python',['./count_repetitions.py', arg1, arg2, arg3, arg4, arg5, arg6], {cwd: 'python_tools'})
    .on('error', (err) => {throw err}); // this is where the python script is located
  pythonScript.stdout.on('data', (data) => {
    resolve(data.toString());
  });

  pythonScript.stderr.on('data', (data) => {
    reject(data.toString());
    return;
  });
});
