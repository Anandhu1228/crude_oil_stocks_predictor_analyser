var express = require('express');
var router = express.Router();
const { spawn } = require('child_process');
const path = require('path'); 


router.get('/', function(req, res, next) {
  res.render("user/testpage")
  return
});


router.post('/send_crude', function(req, res, next) {
  const { Date, Adj_Close, Close, Open, Volume } = req.body;
  const pythonScriptPath = path.join(__dirname, '../machine_models/crude_stock_predictor.py');
  const pythonProcess = spawn('python', [pythonScriptPath, Date, Adj_Close, Close, Open, Volume]);
  
  let result = '';
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send('Python script execution failed');
    }

    try {
      const prediction = JSON.parse(result);
      console.log("PREDICTION :", prediction)
      res.json(prediction);
    } catch (error) {
      console.error('Error parsing Python script output:', error);
      res.status(500).send('Failed to parse prediction result');
    }
  });
});


router.get('/analyse_trends', function(req, res, next) {
  res.render("user/analyse")
  return
});


router.post('/send_crude_analyse', function(req, res, next) {
  const { Year, Month, Criteria } = req.body;
  const pythonScriptPath = path.join(__dirname, '../machine_models/crude_stock_analysis.py');
  const pythonProcess = spawn('python', [pythonScriptPath, Year, Month, Criteria]);

  let result = '';
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send('Python script execution failed');
    }

    try {
      const parsedResult = JSON.parse(result);
      if (parsedResult.error) {
        return res.status(400).json({ error: parsedResult.error });
      }
      return res.json(parsedResult);
    } catch (error) {
      return res.status(500).json({ error: 'Failed to parse Python script output' });
    }
  });
});



module.exports = router;
