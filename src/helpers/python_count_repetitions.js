
module.exports = () => new Promise((resolve, reject) => {
  const spawn = require('child_process').spawn;
  const pythonScript = spawn('python',['count_repetitions.py'], {cwd: 'python_tools'}); // this is where the python script is located
  pythonScript.stdout.on('data', (data) => {
    resolve(data.toString());
  });
  pythonScript.stderr.on('data', (data) => {
    reject(data.toString());
    return;
  });
});
