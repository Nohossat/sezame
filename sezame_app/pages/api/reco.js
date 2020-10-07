const formidable = require('formidable');
const axios = require('axios');

// first we need to disable the default body parser
export const config = {
    api: {
      bodyParser: false,
      externalResolver: true
  }
}

export default (req, res) => {
    if (req.method === 'POST') {

        const form = formidable();
        res.setHeader('Content-Type', 'application/json');

        form.parse(req, (err, fields, files) => {
            if (err) {
                console.dir(err);
                res.statusCode = 500;
                res.end(JSON.stringify({ success: false, error: err }));
            }

            axios.post('http://127.0.0.1:5000/recognize', files)
            .then(function (response) {
                console.dir(response.data);
                res.statusCode = 200;
                res.end(JSON.stringify({ success: true, data: response.data }));
            })
            .catch(function (error) {
                console.dir(error);
                res.statusCode = 500;
                res.end(JSON.stringify({ success: false, error: error }));
            });
        });
      }
      return "false"
  }