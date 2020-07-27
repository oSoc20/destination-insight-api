module.exports = (arg1, arg2, arg3) => new Promise((resolve, reject) => {
  const spawn = require('child_process').spawn;
  // spawn(command, [arg1, args], {options})
  // spawn(<string>, string[], Object)
  // arg1 is the script we want to run
  // args are aditional arguments all separated by a ","
  // options is, well, aditional options

  // call the python script from the script's directory (cwd)
  const pythonScript = spawn('python3',['./searches_by_hour.py', arg1, arg2, arg3], {cwd: 'python_tools'})
    .on('error', (err) => {throw err}); // this is where the python script is located

    // this script will return a json with the amount of searches by hour and day of the week (total)
    // arg1: start date, inclusive (YYYY-MM-DD)
    // arg2: end date, inclusive (YYYY-MM-DD)
    // arg3: date type {'travel', 'request'}
    // command example: python searches_by_hour.py 2020-01-01 2021-01-01 travel

    pythonScript.stderr.on('data', (data) => {
      console.log(`python_searches_by_hour stderr: ${data}`);
      reject(data.toString());
      return;
    });

    pythonScript.stdout.on('data', (data) => {
      resolve(data.toString());
      // At the end of the python script we can find the following 2 lines of code:
      // print(result)
      // sys.stdout.flush()
      // these will let us 'catch' that data and be able to use it on our side
    });
});
