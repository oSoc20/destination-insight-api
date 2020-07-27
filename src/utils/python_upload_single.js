module.exports = (arg2) => new Promise((resolve, reject) => {
  const spawn = require('child_process').spawn;

  // spawn(command, [arg1, args], {options})
  // spawn(<string>, string[], Object)
  // arg1 is the script we want to run
  // args are aditional arguments all separated by a ","
  // options is, well, aditional options

  // call the python script from the script's directory (cwd)
  const pythonScript = spawn('python3',['./upload_single.py', 'uploads', arg2], {cwd: 'python_tools'})
    .on('error', (err) => {
      console.log('Failed to start python_upload_single');
      throw err;
    }); // this is where the python script is located

    // this script will check if the file has already been uploaded, clean the data, and upload it
    // arg1: name of the directory that contains the file
    // arg2: name of the file to upload

  pythonScript.stdout.on('data', (data) => {
    console.log(data.toString());
  })

  pythonScript.stderr.on('data', (err) => {
    //console.log(`python_upload_single stderr: ${err}`);
    const error = `python_upload_single stderr: ${err.toString()}`;
    reject(error);
    return;
  });

  pythonScript.on('close', (code) => {
    resolve('closed');
  });
});
