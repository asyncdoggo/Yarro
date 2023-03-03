import * as argon2 from "argon2";
import { Router } from 'express';
import User from '../../models/user.js';
import { generateAccessToken } from "../../middlewares/jwt.js";
import mongoose from "mongoose";



var loginRouter = Router();

// Login
loginRouter.put('/', async function (req, res) {
    try {
        const user = await User.findOne({
            username: req.body.username
        })

        if (user == null) {
            return res.status(404).json({ message: "Cannot find user" });
        }
        const pwhash = user.password
        if (!await argon2.verify(pwhash, req.body.password)) {
            return res.status(400).json({ message: "Password is incorrect" })
        }

        const token = generateAccessToken(user.username, user._id);
        res.setHeader(`Set-Cookie`, `token=${token}; Secure; HttpOnly; Path=/; SameSite=Strict`)
        return res.status(201).json({ message: "success", userId: user.userId, username: user.username });
    }
    catch (err) {
        console.log(err)
        return res.status(400).json(err.code);
    }
});

// Get users
loginRouter.get('/', async function (req, res) {
    try {
        const user = await User.find()
        res.json(user)
    }
    catch (err) {
        res.status(500).json({ message: err.message })
    }

})


// Register
loginRouter.post('/', async function (req, res) {
    console.log(req.body)
    try {
        const pwhash = await argon2.hash(req.body.password);

        const user = new User({
            _id: new mongoose.Types.ObjectId(),
            username: req.body.username,
            password: pwhash,
            email: req.body.email,
            confirmed: false
        })
        const newUser = await user.save();
        let token = generateAccessToken(newUser.username, newUser._id);
        res.setHeader(`Set-Cookie`, `token=${token}; Secure; HttpOnly; Path=/; SameSite=Strict`)
        return res.status(201).json({ message: "success", userId: user.userId, username: user.username });
    }
    catch (err) {
        console.log(err)
        return res.status(400).json({ message: err.code })
    }
})

export default loginRouter;
