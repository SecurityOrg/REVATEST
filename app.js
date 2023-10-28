const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

const SECRET_KEY = 'super_secret_key';


const users = {
  admin: { password: 'admin_pass', secret: 'Admin Secret Message' },
  user: { password: 'user_pass', secret: 'User Secret Message' },
};

app.get('/', (req, res) => {
  res.send('Welcome to the Vulnerable App!');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  


  if (users[username] && users[username].password === password) {

    res.cookie('username', username, { signed: true });
    res.send(`<h2>Welcome, ${username}!</h2><a href='/secret'>Go to Secret Page</a>`);
  } else {
    res.status(401).send('Invalid credentials!');
  }
});

app.get('/secret', (req, res) => {
  const username = req.signedCookies.username;
  
  if (username) {
    res.send(`<h2>${username}'s Secret Message: ${users[username].secret}</h2>`);
  } else {
    res.status(403).send('You must be logged in to view the secret message Test!');
  }
});

app.listen(3000, () => {
  console.log('Vulnerable App is running on http://localhost:3000');
});
