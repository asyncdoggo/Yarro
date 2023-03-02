import { Router } from 'express';
import jsonwebtoken from 'jsonwebtoken';
import { tokenRequired } from '../../middlewares/jwt.js';
import User from '../../models/user.js';
var indexRouter = Router();

indexRouter.get('/', async function (req, res) {
  try {
    const token = req.cookies.token
    if (token == undefined) {
      return res.render('index.html');
    }

    let userId;
    jsonwebtoken.verify(token, process.env.TOKEN_SECRET, (err, data) => {
      if (err) return res.render("index.html")
      userId = data.userId
    })

    const user = await User.find({
      _id: userId,
      confirmed: true
    })

    if (user) {
      return res.render("main.html")
    }
    else {
      return res.render("confirmemail.html")
    }
  }
  catch (err) {
    return res.render("index.html")
  }
});


indexRouter.get("/register", async function (req, res) {
  const token = req.cookies.token

  try {
    let userId;
    jsonwebtoken.verify(token, process.env.TOKEN_SECRET, (err, data) => {
      if (err) res.render("register.html")
      userId = data.userId
    })
    const user = await User.find({
      _id: userId,
      confirmed: true
    })

    if (user) {
      res.redirect("/")
    }
    else {
      res.render("confirmemail.html")
    }
  }
  catch (err) {
    res.render("register.html")
  }
})

export default indexRouter;
