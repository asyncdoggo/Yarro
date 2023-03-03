import { Router } from 'express';
import jsonwebtoken from 'jsonwebtoken';
import multer from 'multer';
import { tokenRequired } from '../../middlewares/jwt.js';
import fs from 'fs';
import { join } from 'path';

import { __dirname } from '../../app.js'

var imageRouter = Router();

const upload = multer(
    {
        dest: 'uploads/'
    }
)


imageRouter.get('/:id', async function (req, res) {
    const id = req.params.id
    const path = join(__dirname, 'public', 'userimages', `${id}.png`)
    if (fs.existsSync(path)) {
        return res.sendFile(path)
    }
    return res.sendFile(join(__dirname, 'public', 'userimages', 'default.png'))
});

//TODO: Complete with user profile 
imageRouter.post("/", tokenRequired, upload.single('uploaded_file'), async function (req, res) {
    const file = req.file
    console.log(file)

})



export default imageRouter;
