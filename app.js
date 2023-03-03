import express, { json, urlencoded } from 'express';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import nunjucks from 'nunjucks';
import indexRouter from './routes/view/index.js';
import { config } from 'dotenv';
import LoginRouter from './routes/api/login.js';
import mongoose from 'mongoose';
import postRouter from './routes/api/post.js';
import imageRouter from './routes/api/image.js';
var app = express();
config()
app.set('view engine', 'nunjucks');

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

mongoose.connect(process.env.DATABASE_URL)
const db = mongoose.connection
mongoose.set('strictQuery', false);

db.on("error", (err) => console.error(err))

db.once('open', () => console.log("connected to db"))


app.use(logger('dev'));
app.use(json());
app.use(urlencoded({ extended: false }));
app.use(cookieParser());
app.use('/static', express.static('public'));

// views 
app.use('/', indexRouter);


// apis
app.use('/api/login', LoginRouter);
app.use('/api/post', postRouter)
app.use('/image', imageRouter)

export default app;
