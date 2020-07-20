module.exports = (arg1, arg2, arg3, arg4, arg5, arg6) => new Promise((resolve, reject) => {
  const spawn = require('child_process').spawn;

  // spawn(command, [arg1, args], {options})
  // spawn(<string>, string[], Object)
  // arg1 is the script we want to run
  // args are aditional arguments all separated by a ","
  // options is, well, aditional options

  // call the python script from the script's directory (cwd)
  const pythonScript = spawn('python',['./count_links.py', arg1, arg2, arg3, arg4, arg5, arg6], {cwd: 'python_tools'})
    .on('error', (err) => {throw err}); // this is where the python script is located

    // this script will return a json table with the top or bottom station pairings by number of searches
    // arg1: start date, inclusive (YYYY-MM-DD)
    // arg2: end date, inclusive (YYYY-MM-DD)
    // arg3: date type {'travel', 'request'}
    // arg4: most or least common stations {'top', 'bottom'}
    // arg5: integer for number of rows to include

    // command example: python count_links.py 2020-05-13 2020-05-14 travel top 10

  pythonScript.stderr.on('data', (data) => {
    console.log(`python_count_links stderr: ${data}`);
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
