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
