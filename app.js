import express, { json, urlencoded } from 'express';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import { config } from 'dotenv';
import LoginRouter from './routes/api/login.js';
import mongoose from 'mongoose';
import postRouter from './routes/api/post.js';
import imageRouter from './routes/api/image.js';
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'


const __dirname = dirname(fileURLToPath(import.meta.url))



var app = express();
config()

mongoose.connect(process.env.DATABASE_URL)
const db = mongoose.connection
mongoose.set('strictQuery', false);

db.on("error", (err) => console.error(err))

db.once('open', () => console.log("connected to db"))

app.use(function (req, res, next) {
    res.header('Content-Type', 'application/json;charset=UTF-8')
    res.header('Access-Control-Allow-Credentials', true)
    res.header('Access-Control-Allow-Methods', "POST, GET, PUT, OPTIONS, PATCH, DELETE")
    res.header(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept'
    )
    res.header('Access-Control-Allow-Origin', "http://localhost:3000")
    next()
})

app.use(logger('dev'));
app.use(json());
app.use(urlencoded({ extended: false }));
app.use(cookieParser());
app.use('/static', express.static('public'));



// apis
app.use('/api/login', LoginRouter);
app.use('/api/post', postRouter)
app.use('/image', imageRouter)

export { __dirname, app };
